from src.utility.SetupUtility import SetupUtility
SetupUtility.setup([])

from src.utility.WriterUtility import WriterUtility
from src.utility.Initializer import Initializer
from src.utility.loader.ObjectLoader import ObjectLoader
from src.utility.CameraUtility import CameraUtility
from src.utility.LightUtility import Light
from mathutils import Matrix, Vector, Euler

from src.utility.RendererUtility import RendererUtility
from src.utility.PostProcessingUtility import PostProcessingUtility

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('camera', help="Path to the camera file, should be examples/basic/camera_positions")
parser.add_argument('scene', help="Path to the scene.obj file, should be examples/basic/scene.obj")
parser.add_argument('output_dir', help="Path to where the final files, will be saved, could be examples/basic/output")
args = parser.parse_args()

Initializer.init()

# load the objects into the scene
objs = ObjectLoader.load(args.scene)

# define a light and set its location and energy level
light = Light()
light.set_type("POINT")
light.set_location([5, -5, 5])
light.set_energy(1000)

# define the camera intrinsics
CameraUtility.set_intrinsics_from_blender_params(1, 512, 512, lens_unit="FOV")

# read the camera positions file and convert into homogeneous camera-world transformation
with open(args.camera, "r") as f:
    for line in f.readlines():
        line = [float(x) for x in line.split()]
        matrix_world = Matrix.Translation(Vector(line[:3])) @ Euler(line[3:6], 'XYZ').to_matrix().to_4x4()
        CameraUtility.add_camera_pose(matrix_world)

# activate normal and distance rendering
RendererUtility.enable_normals_output()
RendererUtility.enable_distance_output()
# set the amount of samples, which should be used for the color rendering
RendererUtility.set_samples(350)

# render the whole pipeline
data = RendererUtility.render()

# post process the data and remove the redundant channels in the distance image
data["distance"] = PostProcessingUtility.trim_redundant_channels(data["distance"])

# write the data to a .hdf5 container
WriterUtility.save_to_hdf5(args.output_dir, data)

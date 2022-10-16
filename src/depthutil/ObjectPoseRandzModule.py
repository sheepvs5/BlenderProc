import numpy as np
import random
 
from src.main.Module import Module
from src.utility.BlenderUtility import check_intersection, check_bb_intersection, get_all_blender_mesh_objects
from src.utility.MeshObjectUtility import MeshObject
from src.utility.object.ObjectPoseSampler import ObjectPoseSampler
 
class ObjectPoseRandzModule(Module):
    def __init__(self, config):
        Module.__init__(self, config)
 
    def run(self):
        def rand(a):
            return random.uniform(-a/2, a/2)
 
        objects_to_sample = self.config.get_list("objects_to_sample", get_all_blender_mesh_objects())
        number = len(objects_to_sample)
        pos_min = self.config.get_vector3d("min")
        pos_max = self.config.get_vector3d("max")
        rel_rand = self.config.get_float("rel_rand", 0)
        grid = [np.linspace(pmin, pmax, int(np.sqrt(number))) for pmin, pmax in zip(pos_min, pos_max)][:2]
        mesh = [m.reshape(-1) for m in np.meshgrid(*grid)]
        distance = [g[1]-g[0] for g in grid]
        regular_grid = [[x + rand(rel_rand*distance[0]), y + rand(rel_rand*distance[1]), z] \
                        for x,y,z in zip(*mesh, np.random.rand(len(grid[0])**2)*(pos_max[2]-pos_min[2])+pos_min[2])]
        
        for i in range(number-len(regular_grid)):
            regular_grid.append([random.uniform(p1,p2) for p1, p2 in zip(pos_min, pos_max)])
        
        random.shuffle(regular_grid)
        for i, obj in enumerate(objects_to_sample):
            obj.location.x = regular_grid[i][0]
            obj.location.y = regular_grid[i][1]
            obj.location.z = regular_grid[i][2]
 
        mobjs = MeshObject.convert_to_meshes(objects_to_sample)
        for mobj in mobjs:
            mobj.set_rotation_euler(self.config.get_vector3d("rot_sampler"))
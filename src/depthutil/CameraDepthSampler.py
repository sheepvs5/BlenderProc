import bpy
import numpy as np
from src.camera.CameraInterface import CameraInterface
from src.utility.Config import Config
from src.utility.ItemCollection import ItemCollection

class CameraDepthSampler(CameraInterface):
    def __init__(self, config):
        CameraInterface.__init__(self, config)

        self.cam_dof_collection = ItemCollection(self._sample_cam_dofs, self.config.get_raw_dict("default_cam_param", {}))

    def run(self):
        """ Sets camera poses. """

        source_specs = self.config.get_list("cam_dofs")
        for i, source_spec in enumerate(source_specs):
            self.cam_dof_collection.add_item(source_spec)

    def _sample_cam_dofs(self, config):
        keys = {"focus_distance": float, "aperture_blades": int, "aperture_rotation": float, "aperture_ratio": float, "aperture_fstop": float} 
        cam_ob = bpy.context.scene.camera
        cam = cam_ob.data

        self._set_cam_intrinsics(cam, Config(self.config.get_raw_dict("intrinsics", {})))

        frame = config.get_int("frame", None)
        if frame is None:
            frame = bpy.context.scene.frame_end
        if bpy.context.scene.frame_end < frame + 1:
            bpy.context.scene.frame_end = frame + 1

        cam.dof.use_dof = True
        for key in keys:
            if config.has_param(key):
                val = config.get_raw_value(key)
                setattr(cam.dof, key, keys[key](val))
                cam.keyframe_insert(data_path='dof.'+key, frame=frame)




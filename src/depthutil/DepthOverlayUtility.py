# v 0.1.0
import bpy
import numpy as np
import random
from src.main.Module import Module
from src.utility.Utility import Utility
from src.utility.WriterUtility import WriterUtility
from src.utility.RendererUtility import RendererUtility
import os
import io
from contextlib import redirect_stdout
from src.depthutil.DepthRegularizerUtility import render_depth
import random

class DepthOverlayUtility(Module):
    def __init__(self, config):
        Module.__init__(self, config)
        
    def run(self):
        number_of_samples = self.config.get_int("number_of_samples", 30)
        key = self.config.get_string("key", "depth_overlay")
        min_depth = self.config.get_float("min_depth", 3.0)
        output_dir = self._determine_output_dir()

        Utility.add_output_entry({
            "key": key,
            "path": os.path.join(output_dir, "depth_overlay_") + "%04d" + ".npy",
            "version": "2.0.0"
        })

        start_frame, end_frame = bpy.context.scene.frame_start+1, bpy.context.scene.frame_end
        for frame in range(start_frame, end_frame):
            depth = self._render_depth_with_overlay_faster(frame, number_of_samples=number_of_samples, min_depth=min_depth)
            self._write_depth_overlay(depth, frame, output_dir=output_dir, key=key)


    def _render_depth_with_overlay(self, frame=0, number_of_samples=30):
        depth = None
        for i in range(number_of_samples):
            bpy.context.scene.cycles.seed = random.randint(0, 10000)
            depth_tmp = np.array(render_depth(self._determine_output_dir(), frame=frame))
            depth_tmp = np.nan_to_num(depth_tmp, nan=1e4, posinf=1e4, neginf=-1e4)
            if depth is not None:
                depth = np.where(depth<depth_tmp, depth, depth_tmp)
            else:
                depth = depth_tmp
        
        return depth

    def _render_depth_with_overlay_faster(self, frame=0, number_of_samples=30, min_depth=3):
        with Utility.UndoAfterExecution(perform_undo_op=True):
            bpy.context.scene.frame_set(frame)
            for a in bpy.data.actions:
                bpy.data.actions.remove(a)
            bpy.context.scene.cycles.use_animated_seed = True
            bpy.context.scene.frame_start = 0
            bpy.context.scene.frame_end = number_of_samples - 1

            RendererUtility.init()
            RendererUtility.set_samples(1)
            RendererUtility.enable_depth_output(Utility.get_temporary_directory(), 'depth_tmp_', 'depth_tmp')
            with redirect_stdout(io.StringIO()):
                bpy.ops.render.render(animation=True, write_still=True)
        
            depth = None
            for frame in range(number_of_samples):
                output_path = Utility.resolve_path(Utility.find_registered_output_by_key("depth_tmp")['path'] % frame)
                depth_tmp = np.array(WriterUtility.load_output_file(output_path))
                depth_tmp = np.nan_to_num(depth_tmp, nan=1e4, posinf=1e4, neginf=-1e4)
                depth_tmp = np.where(depth_tmp>min_depth, depth_tmp, 1e4)
                if depth is not None:
                    depth = np.where(depth<depth_tmp, depth, depth_tmp)
                else:
                    depth = depth_tmp
                os.remove(output_path)

            return depth

    def _write_depth_overlay(self, depth, frame, output_dir, key="depth_overlay"):
        if output_dir is None:
            output_dir = Utility.get_temporary_directory()

        depth_overlay_output = Utility.find_registered_output_by_key(key)
        path = Utility.resolve_path(depth_overlay_output['path'] % frame)
        np.save(path, depth)        
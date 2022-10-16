import bpy
import numpy as np
import random
from src.main.Module import Module
from src.utility.Config import Config
from src.utility.Utility import Utility
from src.utility.WriterUtility import WriterUtility
from src.provider.getter.Entity import Entity
from src.utility.RendererUtility import RendererUtility
import os
import io
from contextlib import redirect_stdout

def render_depth(output_dir, frame=0, undo_op=True):
    with Utility.UndoAfterExecution(perform_undo_op=undo_op):
        if output_dir is None:
            output_dir = Utility.get_temporary_directory()
        
        bpy.context.scene.frame_start = frame
        bpy.context.scene.frame_end = frame
        bpy.context.scene.frame_set(frame)
        RendererUtility.init()
        RendererUtility.set_samples(1)
        RendererUtility.enable_depth_output(output_dir, 'depth_tmp_', 'depth_tmp')
        with redirect_stdout(io.StringIO()):
            bpy.ops.render.render(animation=False, write_still=True)

        output_path = Utility.resolve_path(Utility.find_registered_output_by_key("depth_tmp")['path'] % frame)
        depth_data = WriterUtility.load_output_file(output_path)
        os.remove(output_path)
        return depth_data

class DepthRegularizerUtility(Module):
    def __init__(self, config):
        Module.__init__(self, config)
        
    def run(self):
        for i in range(self.config.get_int("iterMax", 10)):
            score, depth_histo = self._evaluate_score()
            print("depth score: {}".format(score))
            if(score<self.config.get_float("score", 0.85)):
                self._regularize(depth_histo)
            else:
                break

    def _calculate_depth_histo(self):
        depth_data = render_depth(self._determine_output_dir())
        depth_histo = np.histogram(depth_data, \
                    bins=self.config.get_int("depth_bins", 5), \
                    range=self.config.get_vector("depth_range", [9.5,10.5]))
        return [depth_histo[0], depth_histo[1]-self.config.get_float("depth_center", 10)]

    def _regularize(self, depth_histo):
        objs = self.config.get_list("objects_to_sample", Entity(Config({"conditions": {"cp_physics": True}})).run())
        sparse, dense = np.argmin(depth_histo[0]), np.argmax(depth_histo[0])
        iterMax = self.config.get_int("items_to_move_at_once", 3)
        count = 0
        for obj in objs:
            if(depth_histo[1][dense]<=obj.location.z<=depth_histo[1][dense+1]):
                obj.location.z = random.uniform(depth_histo[1][sparse], depth_histo[1][sparse+1])
                count+=1
                if(count>=iterMax):
                    break

    def _evaluate_score(self):
        depth_histo = self._calculate_depth_histo()
        return np.min(depth_histo[0])/np.max(depth_histo[0]), depth_histo

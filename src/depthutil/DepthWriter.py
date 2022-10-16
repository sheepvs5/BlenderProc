from src.utility.SetupUtility import SetupUtility
SetupUtility.setup_pip(["h5py"])
from src.writer.WriterInterface import WriterInterface
from src.utility.WriterUtility import WriterUtility
from src.utility.Utility import Utility
import numpy as np
import os
import h5py
import bpy

class DepthWriter(WriterInterface):
    def __init__(self, config):
        WriterInterface.__init__(self, config)
        self.dmin = self.config.get_float("dmin", 9)
        self.dmax = self.config.get_float("dmax", 11)
        self.id = self.config.get_int("id", None)
        self.write_all_depth = self.config.get_bool("write_all_depth", False)
        self.additional_key = self.config.get_string("additional_key", None)

    def run(self):
        DepthWriter.write(self._determine_output_dir(False), self.dmin, self.dmax, self.id, self.write_all_depth, self.additional_key)

    @staticmethod
    def _normalize_depth(im, dmin, dmax):
        norm_im = (im - dmin) / (dmax - dmin) * 255
        norm_im[norm_im < 0] = 0
        norm_im[norm_im > 255] = 255
        return np.round(norm_im).astype(np.uint8)

    @staticmethod
    def write(output_dir, dmin, dmax, id=None, write_all_depth=False, additional_key=None):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        DepthWriter._write_frames(output_dir, dmin, dmax, id, write_all_depth, additional_key)

    @staticmethod
    def _write_frames(output_dir, dmin, dmax, id=None, write_all_depth=False, additional_key=None):
        if id is not None:
            hdf5_path = os.path.join(output_dir, "{:06}.hdf5".format(id))
        else:
            files = os.listdir(output_dir)
            files = [file for file in files if ".hdf5" in file]
            count = 0
            while ("{:06}.hdf5".format(count) in files):
                count += 1
            hdf5_path = os.path.join(output_dir, "{:06}.hdf5".format(count))

        with h5py.File(hdf5_path, "w") as f:
            for frame_id in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
                bpy.context.scene.frame_set(frame_id)

                if(frame_id==0):
                    rgb_output = Utility.find_registered_output_by_key("colors")
                    rgb_data = WriterUtility.load_output_file(Utility.resolve_path(rgb_output['path'] % frame_id))
                    WriterUtility._write_to_hdf_file(f, 'color', rgb_data)
                    depth_output = Utility.find_registered_output_by_key("depth")
                    depth_data = WriterUtility.load_output_file(Utility.resolve_path(depth_output['path'] % frame_id))
                    norm_depth_data = DepthWriter._normalize_depth(depth_data, dmin, dmax)
                    WriterUtility._write_to_hdf_file(f, 'depth', norm_depth_data)

                else:
                    rgb_data = WriterUtility.load_output_file(Utility.resolve_path(rgb_output['path'] % frame_id))
                    WriterUtility._write_to_hdf_file(f, '{:06}'.format(frame_id-1), rgb_data) 
                    if write_all_depth:
                        depth_data = WriterUtility.load_output_file(Utility.resolve_path(depth_output['path'] % frame_id))
                        norm_depth_data = DepthWriter._normalize_depth(depth_data, dmin, dmax)
                        WriterUtility._write_to_hdf_file(f, 'depth_{:06}'.format(frame_id-1), norm_depth_data)

                    if additional_key is not None:
                        additional_output = Utility.find_registered_output_by_key(additional_key)
                        additional_data = np.load(Utility.resolve_path(additional_output['path'] % frame_id))
                        norm_add_data = DepthWriter._normalize_depth(additional_data, dmin, dmax)
                        WriterUtility._write_to_hdf_file(f, 'depth_additional_{:06}'.format(frame_id-1), norm_add_data)
                
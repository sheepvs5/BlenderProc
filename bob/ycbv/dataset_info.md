# BOP DATASET: YCB-Video [1]


## Object models

models - Based on models "textured_simple.obj" from the original dataset.
models_fine - Based on models "textured.obj" from the original dataset.

The original 3D object models from [1] were 1) converted from meters to
millimeters and 2) the centers of their 3D bounding boxes were aligned with the
origin of the model coordinate system, i.e. the models were translated by the
vectors below (mm). The ground-truth annotations were converted correspondingly.

Object 01 (002_master_chef_can): [1.3360, -0.5000, 3.5105]
Object 02 (003_cracker_box): [0.5575, 1.7005, 4.8050]
Object 03 (004_sugar_box): [-0.9520, 1.4670, 4.3645]
Object 04 (005_tomato_soup_can): [-0.0240, -1.5270, 8.4035]
Object 05 (006_mustard_bottle): [1.2995, 2.4870, -11.8290]
Object 06 (007_tuna_fish_can): [-0.1565, 0.1150, 4.2625]
Object 07 (008_pudding_box): [1.1645, -4.2015, 3.1190]
Object 08 (009_gelatin_box): [1.4460, -0.5915, 3.6085]
Object 09 (010_potted_meat_can): [2.4195, 0.3075, 8.0715]
Object 10 (011_banana): [-18.6730, 12.1915, -1.4635]
Object 11 (019_pitcher_base): [5.3370, 5.8855, 25.6115]
Object 12 (021_bleach_cleanser): [4.9290, -2.4800, -13.2920]
Object 13 (024_bowl): [-0.2270, 0.7950, -2.9675]
Object 14 (025_mug): [-8.4675, -0.6995, -1.6145]
Object 15 (035_power_drill): [9.0710, 20.9360, -2.1190]
Object 16 (036_wood_block): [1.4265, -2.5305, 17.1890]
Object 17 (037_scissors): [7.0535, -28.1320, 0.0420]
Object 18 (040_large_marker): [0.0460, -2.1040, 0.3500]
Object 19 (051_large_clamp): [10.5180, -1.9640, -0.4745]
Object 20 (052_extra_large_clamp): [-0.3950, -10.4130, 0.1620]
Object 21 (061_foam_brick): [-0.0805, 0.0805, -8.2435]


## Training and test images

train_real - Real images listed in "YCB_Video_Dataset/image_sets/train.txt" [1].
train_synt - 80K synthetic images provided with the original dataset [1].
test - Real images listed in "YCB_Video_Dataset/image_sets/val.txt" [1].


## Subset of test images used for the BOP Challenge 2019

The ground-truth 6D object poses are of a low quality in some images from the
original test set. For the BOP Challenge 2019, we have manually selected 75
images (with higher-quality ground-truth poses) from each of the 12 test scenes.
The selected images are a subset of images listed in
"YCB_Video_Dataset/image_sets/keyframe.txt" [1]. The list of selected images
can be found in file test_targets_bop19.json.


## Cameras

camera_uw.json - Used to capture images in scenes 0000-0059.
camera_cmu.json - Used to capture images in scenes 0060-0091.


## Dataset format

General information about the dataset format can be found in:
https://github.com/thodan/bop_toolkit/blob/master/docs/bop_datasets_format.md


## References

[1] Xiang et al., "PoseCNN: A Convolutional Neural Network for 6D Object Pose
    Estimation in Cluttered Scenes",
    RSS 2018, web: https://rse-lab.cs.washington.edu/projects/posecnn/


## License

Copyright (c) 2017 Robotics and State Estimation Lab at The University of Washington

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

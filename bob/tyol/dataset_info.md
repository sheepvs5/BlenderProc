# BOP DATASET: Toyota Light [1]


## Dataset parameters

* Objects: 21
* Object models: Mesh models with surface color and normals.
* Training images: 51576 rendered images (2455 per object)
* Distribution of the ground truth poses in training images:
    * Range of object distances: 490 mm
    * Azimuth range: 0 - 360 deg
    * Elevation range: -70 - 80 deg
* Test images: 1680 (around 80 per object)
* Distribution of the ground truth poses in test images:
    * Range of object distances: 492.29 - 1253.06 mm
    * Azimuth range: 3.13 - 359.24 deg
    * Elevation range: -67.90 - 76.13 deg


## Lighting conditions and backgrounds

The test images were captured under 5 different lighting conditions and with
4 different backgrounds (yellow, gray, checker and flower tablecloth).


## Training images

The training images were obtained by rendering the object models from a densely
sampled view sphere with the radius of 500 mm and the elevation range of -90 -
90 deg.


## Dataset format

General information about the dataset format can be found in:
https://github.com/thodan/bop_toolkit/blob/master/docs/bop_datasets_format.md


## References

[1] Hodan, Michel et al., "BOP: Benchmark for 6D Object Pose Estimation",
    ECCV 2018, web: http://bop.felk.cvut.cz

# BOP DATASET: HomebrewedDB dataset, Kaskman et al. [1]


## Dataset parameters

* Objects: 33
* Object models: Mesh models with surface color and normals.
* Test scenes: 13
* Validation images: 4420 for each of 2 sensors
* Test images: 13000 for each of 2 sensors
* Distribution of the ground truth poses in test images:
 * Range of object distances: 438.24 - 1416.97 mm 
 * Azimuth range: 0 - 360 deg
 * Elevation range: -90 - 90 deg
	

## About HomebrewedDB

The HomebrewedDB dataset targets the task of single instance, multiple object
detection. It focuses on 3 main aspects:

1. Varying scene complexity: The scenes vary in the number of objects and the
amount of occlusion and clutter.

2. Domain adaptation: The dataset targets evaluating robustness of a method with
respect to severe illumination and texture changes.

3. Scalability: Targets evaluation of method's scalability with respect to a
large number of objects.


## Subset of HomebrewedDB included in the BOP Challenge 2019/2020

3 scenes from the full HomebrewedDB dataset are included:

* Scene 3. Present objects: 4, 9, 19, 29.
* Scene 5. Present objects: 3, 12, 15, 22, 23.
* Scene 13. Present objects: 1, 4, 8, 10, 17, 18, 32, 33.


## References

[1] Kaskman et al. "HomebrewedDB: RGB-D Dataset for 6D Pose Estimation of 3D Objects",
ICCVW 2019, web: http://campar.in.tum.de/personal/ilic/homebreweddb/index.html

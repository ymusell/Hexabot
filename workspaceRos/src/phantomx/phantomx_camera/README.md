# phantomx_camera

ROS package providing scripts and files related to image processing of cracks localisation and positioning.

## test_images

Test images for ttrying out image processing algorithms outside ROS architecture.

## src

Folder containing the scripts.

### visualize_camera

Script that subscribes to the robot's RGBD camera and returns points of a crack (if any is detected) in the robot's coordinate system.

This file is to be included in the general .launch.

### camera_lib

Library used by visualize_camera.

### id_on_test_image

Library used for testing purposes.

### sort fissures

Script that subscribes the current points of a fissure, it will classify each crack, count and record them.

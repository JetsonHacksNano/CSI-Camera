# CSI-Camera
Simple example of using a CSI-Camera (like the Raspberry Pi Version 2 camera) with the NVIDIA Jetson Nano Developer Kit.
The camera should be installed in the MIPI-CSI Camera Connector on the carrier board. The pins on the camera ribbon should face the Jetson Nano module.

There are two demos:

simple_camera.py reads from the camera and displays to a window on the screen using OpenCV:

$ python simple_camera.py

face_detect.py reads from the camera and uses  Haar Cascades to detect faces and eyes:

$ python face_detect.py

Haar Cascades is a machine learning based approach where a cascade function is trained from a lot of positive and negative images. The function is then used to detect objects in other images. 

See: https://docs.opencv.org/3.3.1/d7/d8b/tutorial_py_face_detection.html 

<h2>Release Notes</h2>

Initial Release March, 2019
* L4T 32.1.0 (JetPack 4.2)
* Tested on Jetson Nano



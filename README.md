# CSI-Camera
Simple example of using a CSI-Camera (like the Raspberry Pi Version 2 camera) with the NVIDIA Jetson Nano Developer Kit.
The camera should be installed in the MIPI-CSI Camera Connector on the carrier board. The pins on the camera ribbon should face the Jetson Nano module.

To test the camera:

$ gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM),width=1024, height=768, framerate=120/1, format=NV12' ! nvvidconv flip-method=0 ! nvegltransform ! nveglglessink -e

There are two demos:

simple_camera.py reads from the camera and displays to a window on the screen using OpenCV:

$ python simple_camera.py

face_detect.py reads from the camera and uses  Haar Cascades to detect faces and eyes:

$ python face_detect.py

Haar Cascades is a machine learning based approach where a cascade function is trained from a lot of positive and negative images. The function is then used to detect objects in other images. 

See: https://docs.opencv.org/3.3.1/d7/d8b/tutorial_py_face_detection.html 

<h2>Notes</h2>
You can use v4l2-ctl to determine the camera capabilities. v4l2-ctl is in the v4l-utils:

$ sudo apt-get install v4l-utils

For the Raspberry Pi V2 camera the output is (assuming the camera is /dev/video0):

```
$ v4l2-ctl --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
	Index       : 0
	Type        : Video Capture
	Pixel Format: 'RG10'
	Name        : 10-bit Bayer RGRG/GBGB
		Size: Discrete 3280x2464
			Interval: Discrete 0.048s (21.000 fps)
		Size: Discrete 3280x1848
			Interval: Discrete 0.036s (28.000 fps)
		Size: Discrete 1920x1080
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.017s (60.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.017s (60.000 fps)
```

<h2>Release Notes</h2>

Initial Release March, 2019
* L4T 32.1.0 (JetPack 4.2)
* Tested on Jetson Nano



# CSI-Camera
Simple example of using a MIPI-CSI(2) Camera (like the Raspberry Pi Version 2 camera) with the NVIDIA Jetson Nano Developer Kit. This is support code for the article on JetsonHacks: https://wp.me/p7ZgI9-19v

The camera should be installed in the MIPI-CSI Camera Connector on the carrier board. The pins on the camera ribbon should face the Jetson Nano module, the stripe faces outward.

The new Jetson Nano B01 developer kit has two CSI camera slots. You can use the sensor_mode attribute with nvarguscamerasrc to specify the camera. Valid values are 0 or 1 (the default is 0 if not specified), i.e.

```
nvarguscamerasrc sensor_id=0
```

To test the camera:

```
# Simple Test
#  Ctrl^C to exit
# sensor_id selects the camera: 0 or 1 on Jetson Nano B01
$ gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! nvoverlaysink

# More specific - width, height and framerate are from supported video modes
# Example also shows sensor_mode parameter to nvarguscamerasrc
# See table below for example video modes of example sensor
$ gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! \
   'video/x-raw(memory:NVMM),width=3280, height=2464, framerate=21/1, format=NV12' ! \
   nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=720' ! \
   nvvidconv ! nvegltransform ! nveglglessink -e

Note: The cameras appear to report differently than show below on some Jetsons. You can use the simple gst-launch example above to determine the camera modes that are reported by the sensor you are using. As an example the same camera from below may report differently on a Jetson Nano B01:

GST_ARGUS: 3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000 

You should adjust accordingly. As an example, for 3264x2464 @ 21 fps on sensor_id 1 of a Jetson Nano B01:
$ gst-launch-1.0 nvarguscamerasrc sensor_id=1 ! \
   'video/x-raw(memory:NVMM),width=3264, height=2464, framerate=21/1, format=NV12' ! \
   nvvidconv flip-method=0 ! 'video/x-raw, width=816, height=616' ! \
   nvvidconv ! nvegltransform ! nveglglessink -e

Also, it's been noticed that the display transform is sensitive to width and height (in the above example, width=816, height=616). If you experience issues, check to see if your display width and height is the same ratio as the camera frame size selected (In the above example, 816x616 is 1/4 the size of 3264x2464).
```

There are several examples:

Note: You may need to install numpy for the Python examples to work, ie $ pip3 install numpy

simple_camera.py is a Python script which reads from the camera and displays to a window on the screen using OpenCV:

$ python simple_camera.py

face_detect.py is a python script which reads from the camera and uses  Haar Cascades to detect faces and eyes:

$ python face_detect.py

Haar Cascades is a machine learning based approach where a cascade function is trained from a lot of positive and negative images. The function is then used to detect objects in other images. 

See: https://docs.opencv.org/3.3.1/d7/d8b/tutorial_py_face_detection.html 

The third example is a simple C++ program which reads from the camera and displays to a window on the screen using OpenCV:

```
$ g++ -std=c++11 -Wall -I/usr/lib/opencv simple_camera.cpp -L/usr/lib -lopencv_core -lopencv_highgui -lopencv_videoio -o simple_camera

$ ./simple_camera
```

The final example is dual_camera.py. This example is for the newer rev B01 of the Jetson Nano board, identifiable by two CSI-MIPI camera ports. This is a simple Python program which reads both CSI cameras and displays them in a window. The window is 960x1080. For performance, the script uses a separate thread for reading each camera image stream. To run the script:

```
$ python3 dual_camera.py
```

The directory 'instrumented' contains instrumented code which can help adjust performance and frame rates.

<h2>Notes</h2>

<h3>Camera Image Formats</h3>
You can use v4l2-ctl to determine the camera capabilities. v4l2-ctl is in the v4l-utils:

$ sudo apt-get install v4l-utils

For the Raspberry Pi V2 camera, typically the output is (assuming the camera is /dev/video0):

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

<h3>GStreamer Parameter</h3>
For the GStreamer pipeline, the nvvidconv flip-method parameter can rotate/flip the image. This is useful when the mounting of the camera is of a different orientation than the default.

```

flip-method         : video flip methods
                        flags: readable, writable, controllable
                        Enum "GstNvVideoFlipMethod" Default: 0, "none"
                           (0): none             - Identity (no rotation)
                           (1): counterclockwise - Rotate counter-clockwise 90 degrees
                           (2): rotate-180       - Rotate 180 degrees
                           (3): clockwise        - Rotate clockwise 90 degrees
                           (4): horizontal-flip  - Flip horizontally
                           (5): upper-right-diagonal - Flip across upper right/lower left diagonal
                           (6): vertical-flip    - Flip vertically
                           (7): upper-left-diagonal - Flip across upper left/low
```

<h2>OpenCV and Python</h2>
Starting with L4T 32.2.1 / JetPack 4.2.2, GStreamer support is built in to OpenCV.
The OpenCV version is 3.3.1 for those versions. Please note that if you are using
earlier versions of OpenCV (most likely installed from the Ubuntu repository), you
will get 'Unable to open camera' errors.
<br>
If you can open the camera in GStreamer from the command line, and have issues opening the camera in Python, check the OpenCV version. 

```
>>>cv2.__version__
```

<h2>Release Notes</h2>

v3.1 Release March, 2020
* L4T 32.3.1 (JetPack 4.3)
* OpenCV 4.1.1
* Tested on Jetson Nano B01
* Tested with Raspberry Pi v2 cameras

v3.0 December 2019
* L4T 32.3.1
* OpenCV 4.1.1.
* Tested with Raspberry Pi v2 camera

v2.0 Release September, 2019
* L4T 32.2.1 (JetPack 4.2.2)
* OpenCV 3.3.1
* Tested on Jetson Nano

Initial Release (v1.0) March, 2019
* L4T 32.1.0 (JetPack 4.2)
* Tested on Jetson Nano



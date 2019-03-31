# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2

# gst_str returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 30fps 
def gst_str(width=1280, height=720, framerate=30) :
    return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (framerate,width,height)

def show_camera():
    cap = cv2.VideoCapture(gst_str(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        window_handle = cv2.namedWindow('CSI Camera', cv2.WINDOW_AUTOSIZE)
        # Window 
        while cv2.getWindowProperty('CSI Camera',0) >= 0:
            ret_val, img = cap.read();
            cv2.imshow('CSI Camera',img)
	    # This also acts as 
            keyCode = cv2.waitKey(30) & 0xff
            # Stop the program on the ESC key
            if keyCode == 27:
               break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print 'Unable to open camera'


if __name__ == '__main__':
    show_camera()

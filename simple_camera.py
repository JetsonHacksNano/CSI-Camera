# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 30fps 
# Flip the image by setting the flip_method to 0
# flip-method         : video flip methods
#                        flags: readable, writable, controllable
#                        Enum "GstNvVideoFlipMethod" Default: 0, "none"
#                           (0): none             - Identity (no rotation)
#                           (1): counterclockwise - Rotate counter-clockwise 90 degrees
#                           (2): rotate-180       - Rotate 180 degrees
#                           (3): clockwise        - Rotate clockwise 90 degrees
#                           (4): horizontal-flip  - Flip horizontally
#                           (5): upper-right-diagonal - Flip across upper right/lower left diagonal
#                           (6): vertical-flip    - Flip vertically
#                           (7): upper-left-diagonal - Flip across upper left/low
def gstreamer_pipeline (width=1280, height=720, framerate=30, flip_method=2) :
    return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv  flip-method=%d ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (framerate,flip_method,width,height)


def show_camera():
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
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

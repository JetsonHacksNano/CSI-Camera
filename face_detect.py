# MIT License
# Copyright (c) 2019 JetsonHacks
# See LICENSE for OpenCV license and additional information

# https://docs.opencv.org/3.3.1/d7/d8b/tutorial_py_face_detection.html
# On the Jetson Nano, OpenCV comes preinstalled
# Data files are in /usr/sharc/OpenCV
import numpy as np
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


def face_detect() :
    face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_eye.xml')
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        cv2.namedWindow('Face Detect', cv2.WINDOW_AUTOSIZE)
        while cv2.getWindowProperty('Face Detect',0) >= 0:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            cv2.imshow('Face Detect',img)
            keyCode = cv2.waitKey(30) & 0xff
            # Stop the program on the ESC key
            if keyCode == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

if __name__ == '__main__':
    face_detect()

# MIT License
# Copyright (c) 2019 JetsonHacks
# See LICENSE for OpenCV license and additional information

# https://docs.opencv.org/3.3.1/d7/d8b/tutorial_py_face_detection.html
# On the Jetson Nano, OpenCV comes preinstalled
# Data files are in /usr/sharc/OpenCV
import numpy as np
import cv2
import threading
from timecontext import Timer

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 30fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

frames_displayed=0
fps_timer=None

def update_fps_stats():
    global frames_displayed
    print("======")
    print("FPS: "+str(frames_displayed))
    frames_displayed=0
 
def start_counting_fps():
    global fps_timer
    print("starting to count fps")
    fps_timer=RepeatTimer(1.0,update_fps_stats)
    fps_timer.start()

def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def face_detect():
    global frames_displayed
    global fps_timer
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
    )
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        try: 
            cv2.namedWindow("Face Detect", cv2.WINDOW_AUTOSIZE)
            # Setup our Frames per second counter
            start_counting_fps()
            while cv2.getWindowProperty("Face Detect", 0) >= 0:
                with Timer() as measure :
                    ret, img = cap.read()
                    print("---")
                    print("Read Cam:" + str(measure.elapsed))
                    before=measure.elapsed
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    print("detectMultipleScale: "+str(measure.elapsed-before))
                    before=measure.elapsed
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        roi_gray = gray[y : y + h, x : x + w]
                        roi_color = img[y : y + h, x : x + w]
                        eyes = eye_cascade.detectMultiScale(roi_gray)
                        for (ex, ey, ew, eh) in eyes:
                            cv2.rectangle(
                                roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
                            )
                    print("eyeCascade: "+str(measure.elapsed-before))
                    print(measure.elapsed)
                    cv2.imshow("Face Detect", img)
                    
                print("Elapsed time: "+str(measure.elapsed))
                frames_displayed = frames_displayed+1
                keyCode = cv2.waitKey(5) & 0xFF
                # Stop the program on the ESC key
                if keyCode == 27:
                    break
        finally:
            fps_timer.cancel()
            fps_timer.join() 

        cap.release()
        # Kill the fps timer
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    face_detect()

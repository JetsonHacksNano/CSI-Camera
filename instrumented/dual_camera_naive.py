# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
from timecontext import Timer
import numpy as np

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen


def gstreamer_pipeline(
    sensor_id=0,
    sensor_mode=3,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            sensor_mode,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    left_cap = cv2.VideoCapture(
        gstreamer_pipeline(flip_method=0,display_width=960,display_height=540,framerate=30), cv2.CAP_GSTREAMER)
    right_cap = cv2.VideoCapture(gstreamer_pipeline(
        flip_method=0, sensor_id=1,display_width=960,display_height=540,framerate=30), cv2.CAP_GSTREAMER)
    if left_cap.isOpened():
        cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            with Timer() as context_time:
                ret_val, left_image = left_cap.read()
                ret_val, right_image = right_cap.read()
                # print(context_time.elapsed)
                # We place both images side by side to show in the window
                camera_images = np.hstack((left_image, right_image))
                cv2.imshow("CSI Cameras", camera_images)
                # cv2.imshow("CSI Camera", left_image)
                # print(context_time.elapsed)

                # This also acts as
                keyCode = cv2.waitKey(20) & 0xFF
            # print(context_time.elapsed)
            # print("---")
            # Stop the program on the ESC key
            if keyCode == 27:
                break
        left_cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()

# MIT License
# Copyright (c) 2019,2020 JetsonHacks
# See license
# A very simple code snippet
# Using two  CSI cameras (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit (Rev B01) using OpenCV
# Drivers for the camera and OpenCV are included in the base image in JetPack 4.3+

# This script will open a window and place the camera stream from each camera in a window
# arranged horizontally.
# The camera streams are each read in their own thread, as if done sequentially there
# is a noticeable lag
# For better performance, the next step would be to experiment with having the window display
# in a separate thread

import cv2
import threading
import numpy as np

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of each camera pane in the window on the screen

left_camera = None
right_camera = None


class CSI_Camera:
    # OpenCV video capture element
    video_capture = None
    # The last captured image from the camera
    image = None
    # The thread where the video capture runs
    read_thread = None

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)
            return

    def start(self):
        # create a thread to read the camera image
        if self.video_capture != None:
            self.read_thread = threading.Thread(target=self.read_image)
            self.read_thread.start()
        return self

    def read_image(self):
        # This is the thread to read images from the camera
        while self.video_capture.isOpened():
            try:
                retval, self.image = self.video_capture.read()
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        self.read_thread = None

    def release(self):
        if self.video_capture != None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread != None:
            self.read_thread.join()


# Currently there are setting frame rate on CSI Camera on Nano through gstreamer
# Here we directly select sensor_mode 3 (1280x720, 59.9999 fps)
def gstreamer_pipeline(
    sensor_id=0,
    sensor_mode=3,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
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


def start_cameras():
    left_camera = CSI_Camera()
    left_camera.open(
        gstreamer_pipeline(
            sensor_id=0,
            sensor_mode=3,
            flip_method=0,
            display_height=540,
            display_width=960,
        )
    )
    right_camera = CSI_Camera()
    right_camera.open(
        gstreamer_pipeline(
            sensor_id=1,
            sensor_mode=3,
            flip_method=0,
            display_height=540,
            display_width=960,
        )
    )

    if left_camera.video_capture.isOpened():
        left_camera.start()
        cv2.namedWindow("Left Camera", cv2.WINDOW_AUTOSIZE)

    if right_camera.video_capture.isOpened():
        right_camera.start()
        cv2.namedWindow("Right Camera", cv2.WINDOW_AUTOSIZE)

    cv2.namedWindow("CSI Cameras", cv2.WINDOW_AUTOSIZE)

    if (
        not left_camera.video_capture.isOpened()
        or not right_camera.video_capture.isOpened()
    ):
        # Cameras did not open, or no camera attached

        print("Unable to open any cameras")
        # TODO: Cleanup
        SystemExit(0)

    while (
        cv2.getWindowProperty("Left Camera", 0) >= 0
        or cv2.getWindowProperty("Right Camera", 0) >= 0
    ):
        # if cv2.getWindowProperty("Left Camera", 0) >= 0 and left_camera.image is not None :
        # cv2.imshow("Left Camera", left_camera.image)

        # if cv2.getWindowProperty("Right Camera", 0) >= 0 and right_camera.image is not None :
        # cv2.imshow("Right Camera", right_camera.image)

        frame = np.hstack((left_camera.image, right_camera.image))
        frame_concat = np.concatenate((left_camera.image, right_camera.image), axis=1)
        cv2.imshow("CSI Cameras", frame_concat)

        # This also acts as
        keyCode = cv2.waitKey(30) & 0xFF
        # Stop the program on the ESC key
        if keyCode == 27:
            break

    left_camera.release()
    right_camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_cameras()

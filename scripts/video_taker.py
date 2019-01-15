"""
This script is useful for capturing video to use as test data.

TODO: We should really nail down the exact settings the camera will use... resolution, shutter speed, etc.ss
"""

import picamera
import sys
import cv2
import time


def record_video(filename):
    with picamera.PiCamera() as camera:
        time.sleep(2)
        camera.resolution = (1024, 768)
        camera.start_recording('{0}.h264'.format(filename))

        try:
            while True:
                camera.wait_recording(10)
        except KeyboardInterrupt:
            print("Control-C caught, stopping recording")
            camera.stop_recording()

        print("Wrote file " + filename)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("the record video script requires the name of the video to be passed in.")
        sys.exit(1)

    filename = sys.argv[1]
    print("Recording video.  Control-C to exit.")
    record_video(filename)

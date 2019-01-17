from smartchoke.targeting.trap_targeter import TrapTargeter
from smartchoke.targeting import show_frame
import cv2
import time
import mock
import unittest


def get_mocked_targeter(filename, start_frame):
    """
    Gets a trap targeter with a modified get_targets
    method that reads from a file instead of the camera,
    allowing us to use pre-recorded test data
    :param filename: Relative path of the test filename
    :param start_frame: Optional frame number to start on.  Useful if there is a lot of boring frames at the start of test data
    :return:
    """
    tt = TrapTargeter()

    def mock_get_targets(self):
        vcap = cv2.VideoCapture(filename)
        mock_pi_array = mock.Mock()

        i = 0

        while vcap.isOpened():
            ret, frame = vcap.read()
            if i < start_frame:
                i += 1
                continue
            mock_pi_array.array = frame

            print("Frame {0}".format(i))
            show_frame("capture", frame, (640, 400))
            if not ret:
                print("Could not read frame of file {0}".format(filename))
                break
            yield self.get_targets_impl(mock_pi_array)
            i += 1

    tt.get_targets = mock_get_targets
    return tt


class TestTrapTargeter(unittest.TestCase):

    def test_identify_pidgeon(self):
        tt = get_mocked_targeter("test_data/test_outside2.h264", start_frame=100)
        print(tt)
        for target in tt.get_targets(tt):
            print(target)

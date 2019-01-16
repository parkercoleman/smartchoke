from smartchoke.targeting.trap_targeter import TrapTargeter
import cv2
import time
import unittest


def get_mocked_targeter(filename):
    """
    Gets a trap targeter with a modified get_targets
    method that reads from a file instead of the camera,
    allowing us to use pre-recorded test data
    :param filename:
    :return:
    """
    tt = TrapTargeter()

    def mock_get_targets(self):
        vcap = cv2.VideoCapture(filename)
        while vcap.isOpened():
            ret, frame = vcap.read()
            print(frame)
            time.sleep(1)
            yield self.get_targets_impl(frame)

    tt.get_targets = mock_get_targets
    return tt


class TestTrapTargeter(unittest.TestCase):

    def test_identify_pidgeon(self):
        tt = get_mocked_targeter("test_data/test_outside2.h264")
        print(tt)
        for target in tt.get_targets(tt):
            print(target)

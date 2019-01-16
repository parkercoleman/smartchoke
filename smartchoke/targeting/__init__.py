import cv2


def show_frame(display_name, frame, resize=None):
    """
    Handy utility function to make displaying frames a bit easier (mostly for debug purposes)
    :param display_name: The name of the window
    :param frame: The frame data
    :param resize: An optional tuple to resize (to fit on smaller screens) i.e (640, 400)
    :return:
    """
    cv2.imshow(display_name, cv2.resize(frame, resize) if resize is not None else frame)
    cv2.waitKey(1) & 0xFF

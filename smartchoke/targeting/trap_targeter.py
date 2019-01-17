"""
This modules defines the Trap Targeter class.  The lifespan of this class is expected to be a single trap pull, there
should be a button on the gun that will reset our target trackers after every shot (basically, once the gun is level
and the shooter is about to call pull).

Once the gun is steady, the background of the image can easily be filtered out.  At that point, once the disk is visible
the OpenCV optical flow algorithm is used to get a vector from the first two frames the disk is visible.

The direction of this vector, combined with the known speed of the projectile (about 40mph) should tell us how fast it is
moving away from the shooter, at which point we can rely on basic physics.

Optical flow code heavily based on this example:
https://docs.opencv.org/3.4/d7/d8b/tutorial_py_lucas_kanade.html

Background subtraction detailed here
https://docs.opencv.org/3.4/db/d5c/tutorial_py_bg_subtraction.html
"""


from smartchoke.targeting.abstracttarget import AbstractTargeter, Target
from smartchoke.targeting import show_frame
import numpy as np
import cv2
import time 


feature_params = dict(maxCorners=25, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0, 255, (100, 3))


class TrapTargeter(AbstractTargeter):
	def __init__(self, debug_mode=False):
		self.debug_mode = debug_mode
		super().__init__()
		self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
		self.prev_frame = None
		self.prev_features = None

	def subtract_background(self, frame):
		"""
		Subtracts background, frame is a numpy array
		:param frame:
		:return:
		"""
		mask = self.fgbg.apply(frame)
		imask = mask > 0
		fg = np.zeros_like(frame, np.uint8)
		fg[imask] = frame[imask]
		return fg, mask

	def detect_features(self, frame):
		return cv2.goodFeaturesToTrack(frame, mask=None, **feature_params)

	def calc_optical_flow(self, frame):
		print(type(self.prev_features[0][0]))
		print(self.prev_features.shape)
		new_features, st, err = cv2.calcOpticalFlowPyrLK(self.prev_frame, frame, self.prev_features, None, **lk_params)

		# Select good points
		good_new = new_features[st == 1]
		good_old = self.prev_features[st == 1]

		return good_old, good_new

	def draw_path(self, frame, good_new, good_old):
		mask = np.zeros_like(frame)
		for i, (new, old) in enumerate(zip(good_new, good_old)):
			a, b = new.ravel()
			c, d = old.ravel()
			mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
			frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
		img = cv2.add(frame, mask)
		return img

	def get_targets_impl(self, frame):
		fg, fg_mask = self.subtract_background(frame.array)
		# TODO: Subtract background returns the foreground and the foreground mask.  We only need the mask to generate contours
		# but we return both to potentially further filter based on color

		#fg_grey = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)
		#ret, thresh = cv2.threshold(fg_grey, 127, 255, 0)
		contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(fg, contours, -1, (0, 255, 0), 3)
		print(len(contours) if contours is not None else "No Contours")
		show_frame("detected", fg, (640, 400))
		return Target(distance=0)



	#  TODO: I don't think I wanna go with the optical flow stuff when contour detection is probably easier and faster.
	#  I'll keep it here just to have it in the repo if i ever wanna look at it again.
	def get_targets_impl_2(self, frame):
		frame = cv2.cvtColor(frame.array, cv2.COLOR_BGR2GRAY)
		fgmask = self.subtract_background(frame).astype('float32')
		features = self.detect_features(fgmask)
		features = features.astype('float32') if features is not None else features

		if self.prev_frame is None:
			self.prev_frame = fgmask.copy()
			self.prev_features = features
			# We can't find a target on the first frame we have, return none.
			return None

		if self.prev_features is None:
			# We can't calculate a target if no features were detected, return none.
			return None

		good_old, good_new = self.calc_optical_flow(fgmask)
		new_img = self.draw_path(fgmask, good_old, good_new)

		show_frame("detected", new_img, (640, 400))

		# Finally update the previous frame and features
		self.prev_frame = fgmask.copy()
		self.prev_features = good_new.reshape(-1, 1, 2)

		return Target(distance=0)

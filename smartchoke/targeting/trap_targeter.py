from smartchoke.targeting.abstracttarget import AbstractTargeter, Target
import numpy as np
import cv2
import time 

lower_hsv = (10, 0, 0)
upper_hsv = (20, 255, 255)


class TrapTargeter(AbstractTargeter):
	def __init__(self, debug_mode=False):
		self.debug_mode = debug_mode
		super().__init__()
		self.i = 0
	
	def get_targets_impl(self, frame):
		self.i += 1
		raw_hsv = cv2.cvtColor(frame.array, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(raw_hsv, lower_hsv, upper_hsv)
		
		imask = mask>0
		orange = np.zeros_like(frame.array, np.uint8)
		orange[imask] = frame.array[imask]
		
		cv2.imshow("Frame", orange)
		key = cv2.waitKey(1) & 0xFF
		
		if self.i > 10:
			print("WRITING IMAGE")
			cv2.imwrite('disk.jpg', orange)
			self.i = 0

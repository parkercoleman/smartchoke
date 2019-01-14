from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from abc import ABC, abstractmethod

class Target():
	"""
	This class encapsulates information about a target.  Currently the only 
	thing we care about is distance from us (in meters) 
	but this could change in the future.
	"""
	def __init__(self, distance):
		self.distance = distance
	
	def __str__(self):
		return "Distance {0} meters".format(self.distance)

class AbstractTargeter(ABC):
	"""
	This class provides access to the camera.  Classes that 
	extend this abstract class should define a get_targets 
	method that returns information about targets.
	"""
	
	def __init__(self):
		self.camera = PiCamera()
		self.camera.resolution = (1920, 1088)
		self.camera.framerate = 30
		self.raw_capture = PiRGBArray(self.camera)
		time.sleep(2) #let the camera warm up
	
	def get_targets(self):
		while True: # TODO: Can put some kind of shutdown() method on the AbstractTargeter to check for here.
			self.camera.capture(self.raw_capture, format="bgr", use_video_port=True)
			yield self.get_targets_impl(self.raw_capture)
			self.raw_capture.truncate(0)
	
	@abstractmethod
	def get_targets_impl(raw_capture):
		pass
	
if __name__ == "__main__":
	# Assume we're in demo mode and simply show whats 
	# being captured by the camera
	
	class DemoTarget(AbstractTargeter):
		def get_targets_impl(self, raw_capture):
			return Target(0)
	
	d = DemoTarget()
	for target in d.get_targets():
		cv2.imshow("Frame", d.raw_capture.array)
		key = cv2.waitKey(1) & 0xFF # This line is actually nessessary for anything to render

	
	
 

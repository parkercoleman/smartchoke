from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

print("Get ready to take a picture in 15 seconds!")
sleep(15)
camera.capture('disk.jpg')

from picamera import PiCamera
from time import sleep

camera = PiCamera()
print("llega1")
# camera.resolution =(1024,768)
camera.start_preview()
print("llega2")
sleep(10)
camera.capture('/home/pi/Desktop/fotopython.jpg')
camera.stop_preview()
print("llega3")
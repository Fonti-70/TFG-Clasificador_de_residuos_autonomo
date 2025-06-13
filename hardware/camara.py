from picamera import PiCamera
from time import sleep
from config import IMAGE_PATH

camera = PiCamera()

def capture_image():
    camera.capture(IMAGE_PATH)
    return IMAGE_PATH

import RPi.GPIO as GPIO

def setup_motion_sensor(pin=18):
    GPIO.setup(pin, GPIO.IN)

def detect_motion(pin=18):
    return GPIO.input(pin) == 1

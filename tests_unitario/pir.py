from gpiozero import MotionSensor
from gpiozero import Servo
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

while True:
    
    i = GPIO.input(11)
    print("el valor esta a ",i)
    time.sleep(3)
    
    
    
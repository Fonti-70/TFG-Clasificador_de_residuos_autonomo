from gpiozero import MotionSensor
from gpiozero import Servo
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN)

GPIO.setup(5,GPIO.OUT)
servo2 = GPIO.PWM(5,50)

GPIO.setup(7,GPIO.OUT)
servo3 = GPIO.PWM(7,50)

GPIO.setup(11,GPIO.OUT)
servo4 = GPIO.PWM(11,50)

GPIO.setup(13,GPIO.OUT)
servo5 = GPIO.PWM(13,50)



i = GPIO.input(3)

while True:
    i=0
    i = GPIO.input(3)
    
    if i==0:
        print ("No se detecta")
        time.sleep(0.1)
    elif i==1:
        print ("se detecta servo2")
        time.sleep(0.1)
        
        servo2.start(0)
        print ("Waiting for 2 seconds")
        time.sleep(2)
        # Turn back to 90 degrees
        print ("Turning back to 90 degrees for 2 seconds")
        servo2.ChangeDutyCycle(7)
        time.sleep(2)

        #turn back to 0 degrees
        print ("Turning back to 0 degrees")
        servo2.ChangeDutyCycle(2)
        time.sleep(0.5)
        servo2.ChangeDutyCycle(0)
        
        print ("se detecta servo3")
        time.sleep(0.1)
        
        servo3.start(0)
        print ("Waiting for 2 seconds")
        time.sleep(2)
        # Turn back to 90 degrees
        print ("Turning back to 90 degrees for 2 seconds")
        servo3.ChangeDutyCycle(7)
        time.sleep(2)

        #turn back to 0 degrees
        print ("Turning back to 0 degrees")
        servo3.ChangeDutyCycle(2)
        time.sleep(0.5)
        servo3.ChangeDutyCycle(0)
        
        print ("se detecta servo4")
        time.sleep(0.1)
        
        servo4.start(0)
        print ("Waiting for 2 seconds")
        time.sleep(2)
        # Turn back to 90 degrees
        print ("Turning back to 90 degrees for 2 seconds")
        servo4.ChangeDutyCycle(7)
        time.sleep(2)

        #turn back to 0 degrees
        print ("Turning back to 0 degrees")
        servo4.ChangeDutyCycle(2)
        time.sleep(0.5)
        servo4.ChangeDutyCycle(0)
        
        print ("se detecta servo5")
        time.sleep(0.1)
        
        servo5.start(0)
        print ("Waiting for 2 seconds")
        time.sleep(2)
        # Turn back to 90 degrees
        print ("Turning back to 90 degrees for 2 seconds")
        servo5.ChangeDutyCycle(7)
        time.sleep(2)

        #turn back to 0 degrees
        print ("Turning back to 0 degrees")
        servo5.ChangeDutyCycle(2)
        time.sleep(0.5)
        servo5.ChangeDutyCycle(0)

#Clean things up at the end
        #servo1.stop()
       # GPIO.cleanup()
       # print ("Goodbye")
    
    
    

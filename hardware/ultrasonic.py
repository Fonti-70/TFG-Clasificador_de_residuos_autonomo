import RPi.GPIO as GPIO
import time

def measure_distance(trig, echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    while GPIO.input(echo) == 0:
        inicio = time.time()

    while GPIO.input(echo) == 1:
        fin = time.time()

    distancia = (fin - inicio) * 343.2 / 2
    return distancia

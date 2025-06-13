import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

TRIG = 31
ECHO = 33

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

distancia = 0

GPIO.output(TRIG,True)
time.sleep(0.00001)
GPIO.output(TRIG,False)

while GPIO.input(ECHO)==0:
    print("escucha")
    inicio = time.time()

while GPIO.input(ECHO)==1:
    print("oye")
    fin = time.time()

tiempo = fin -inicio
distancia = (tiempo/2) * 343.200  # en metros 

print("la distancia es " , distancia)
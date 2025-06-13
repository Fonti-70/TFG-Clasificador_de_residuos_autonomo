from picamera import PiCamera
from gpiozero import MotionSensor
from gpiozero import Servo
import RPi.GPIO as GPIO

from rpi_lcd import LCD

import time

import tensorflow as tf
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K
from tensorflow.python.keras import applications
from PIL import Image, ImageOps #Install pillow instead of PIL

import PIL.Image
if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
    PIL.Image.Resampling = PIL.Image
# Now PIL.Image.Resampling.BICUBIC is always recognized.




def predicion(img,modelo,clases):
    
    #importacion del modelo
    model = modelo
    class_names = clases
    
    #preparamos la imagen antes de poder realizar la inferencia
    
    #se crea el vector que contendra los input
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # La imagen es cargada y convertida a formato RGB 
    image = Image.open(img).convert('RGB')

    #redimensionamos la imagen a 224x224 y la recortamos con LANC todos los pixeles contribuyen a las salida 
    #esto para no tener problemas con las dimensiones de las entradas 
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    #cargamos la imagen dentro de un array 
    image_array = np.asarray(image)

    # Normalizamos los valores del vector para poder ser procesado como fueron procesado los datos de entrenamiento
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # cargamos el vector normalizado en el array anteriormente creado de tipo np.array
    data[0] = normalized_image_array

    # hacemos la inferencia nos quedamos con el indice con mayor probabilidad y devolvemos
    # su id y el nombre de la clase a la que corresponde
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]

    return class_name


def aperturaTapa(servo):
    
    servo.start(0)
    
    
    # El servo girara 90 grados y abrira la tapa durante 2 segundos
    servo.ChangeDutyCycle(7)
    time.sleep(2)

    # el servo motor volvera a su posicion de inicio cerrando la tapa
    servo.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
    
    

def calcularCapacidad(TRIG,ECHO):
    
    distancia = 0
    v_sonido = 343.200 #m/s
    
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)

    while GPIO.input(ECHO)==0:
        print("escucha")
        inicio = time.time()

    while GPIO.input(ECHO)==1:
        print("oye")
        fin = time.time()

    tiempo = fin -inicio #s
    
    distancia = (tiempo/2) * v_sonido # en metros
    print("la distancia es :" ,distancia)
    return distancia
    

##---------------------main--------##
    
# Variable globales

tapaGris = str(0)
tapaAmarilla = str(1)
tapaVerde = str(2)
tapaAzul = str(3)

Cap_max = 1000

#iniciamos pantalla LCD
lcd = LCD()

# Cargamos modelo y las clases 
print("Cargando modelo ...")
lcd.text("Carga modelo",1)
model = tf.keras.models.load_model('keras_model.h5',compile=False)
class_names = open('labels .txt', 'r').readlines()
print("modelo cargado")
lcd.text("Cargado",1)
time.sleep(1)



#iniciamos los sensores

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)



#sensor de movimiento 

GPIO.setup(18,GPIO.IN)  
sensorMov = GPIO.input(18)

# Motores que abren los cubos 

GPIO.setup(7,GPIO.OUT)
amarillo = GPIO.PWM(7,50)

GPIO.setup(11,GPIO.OUT)
azul = GPIO.PWM(11,50)

GPIO.setup(13,GPIO.OUT)
verde = GPIO.PWM(13,50)

GPIO.setup(15,GPIO.OUT)
gris = GPIO.PWM(15,50)

# iniciamos camara 
camera = PiCamera()

#Sensores de capacidad

amarillo_Trig = 38
amarillo_Echo = 40

GPIO.setup(amarillo_Trig,GPIO.OUT)
GPIO.setup(amarillo_Echo,GPIO.IN)

azul_Trig = 35
azul_Echo = 37

GPIO.setup(azul_Trig,GPIO.OUT)
GPIO.setup(azul_Echo,GPIO.IN)

verde_Trig = 31
verde_Echo = 33

GPIO.setup(verde_Trig,GPIO.OUT)
GPIO.setup(verde_Echo,GPIO.IN)

gris_Trig = 32
gris_Echo = 36

GPIO.setup(gris_Trig,GPIO.OUT)
GPIO.setup(gris_Echo,GPIO.IN)




while True:
    print(sensorMov)
    time.sleep(1)
    sensorMov = GPIO.input(18)
    
    if sensorMov == 1:
        
        print("camara ON ")
        lcd.text("Tomando foto",1)
        #camera.start_preview()
        #time.sleep(3)
        camera.capture('/home/pi/Desktop/ejemplo.jpg')
        #camera.stop_preview()
        lcd.text("foto tomada",1)
        time.sleep(1)
        lcd.text("Haciendo",1)
        lcd.text("predicion",2)
        print("foto hecha")
        res = predicion("ejemplo.jpg",model,class_names)
        print("predicion = ",res[0])
        
        if res[0] == tapaGris:
            
            if calcularCapacidad(gris_Trig,gris_Echo) < Cap_max:
                aperturaTapa(gris)
            else:
                print("capacidad maxima alcanzada gris")
                lcd.text("cubo gris",1)
                lcd.text("lleno",2)
                time.sleep(1.3)
        
        if res[0] == tapaAzul:
            
            if calcularCapacidad(azul_Trig,azul_Echo) < Cap_max:
                aperturaTapa(azul)
            else:
                print("capacidad maxima alcanzada azul")
                lcd.text("cubo azul",1)
                lcd.text("lleno",2)
                time.sleep(1.3)
            
            
        if res[0] == tapaAmarilla:
            
            if calcularCapacidad(amarillo_Trig,amarillo_Echo) < Cap_max:
                aperturaTapa(amarillo)
            else:
                print("capacidad maxima alcanzada amarillo")
                lcd.text("cubo amar",1)
                lcd.text("lleno",2)
                time.sleep(1.3)
        
        
        if res[0] == tapaVerde:
            
            if calcularCapacidad(verde_Trig,verde_Echo) < Cap_max:
                aperturaTapa(verde)
            else:
                print("capacidad maxima alcanzada verde")
                lcd.text("cubo verde",1)
                lcd.text("lleno",2)
                time.sleep(1.3)
        lcd.clear()
    else:
        print("no se detecta nada ")
        lcd.text("esperando",1)
        time.sleep(1)
        lcd.clear()


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

inicio = time.time()

print("cargando modelo ...")

model = tf.keras.models.load_model('keras_model.h5',compile=False)
class_names = open('labels .txt', 'r').readlines()

print("modelo cargado")

fin = time.time()

print("tiempo en cargar el modelo ",fin-inicio)

inicio = time.time()



data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image = Image.open('ejemplo.jpg').convert('RGB')

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

#turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image

normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array

# run the inference

prediction = model.predict(data)

index = np.argmax(prediction)
class_name = class_names[index]


print('Class:', class_name, end='')

fin = time.time()

print("tiempo en hacer predicion ",fin-inicio)


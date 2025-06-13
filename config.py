# config.py

CAP_MAX = 1.0  # metros
IMAGE_PATH = '/home/pi/Desktop/ejemplo.jpg'
MODEL_PATH = 'model/keras_model.h5'
LABELS_PATH = 'labels .txt'

TAPAS = {
    '0': {'nombre': 'gris', 'pin': 15, 'trig': 32, 'echo': 36},
    '1': {'nombre': 'amarillo', 'pin': 7, 'trig': 38, 'echo': 40},
    '2': {'nombre': 'verde', 'pin': 13, 'trig': 31, 'echo': 33},
    '3': {'nombre': 'azul', 'pin': 11, 'trig': 35, 'echo': 37}
}
EOF && \
cat > hardware/camera.py << 'EOF'
from picamera import PiCamera
from time import sleep
from config import IMAGE_PATH

camera = PiCamera()

def capture_image():
    camera.capture(IMAGE_PATH)
    return IMAGE_PATH
EOF && \
cat > hardware/lcd_display.py << 'EOF'
from rpi_lcd import LCD
import time

lcd = LCD()

def show_message(line1="", line2="", delay=1):
    lcd.text(line1, 1)
    lcd.text(line2, 2)
    time.sleep(delay)
    lcd.clear()
EOF && \
cat > hardware/movement.py << 'EOF'
import RPi.GPIO as GPIO

def setup_motion_sensor(pin=18):
    GPIO.setup(pin, GPIO.IN)

def detect_motion(pin=18):
    return GPIO.input(pin) == 1
EOF && \
cat > hardware/servo.py << 'EOF'
import RPi.GPIO as GPIO
import time

def open_lid(pin):
    servo = GPIO.PWM(pin, 50)
    servo.start(0)
    servo.ChangeDutyCycle(7)  # Abrir
    time.sleep(2)
    servo.ChangeDutyCycle(2)  # Cerrar
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
    servo.stop()
EOF && \
cat > hardware/ultrasonic.py << 'EOF'
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
EOF && \
cat > model/loader.py << 'EOF'
import tensorflow as tf
from config import MODEL_PATH, LABELS_PATH

def load_model_and_labels():
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    labels = open(LABELS_PATH, 'r').readlines()
    return model, labels
EOF && \
cat > model/predictor.py << 'EOF'
from PIL import Image, ImageOps
import numpy as np
from config import IMAGE_PATH

def predict_class(model, class_names):
    size = (224, 224)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(IMAGE_PATH).convert("RGB")
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized
    prediction = model.predict(data)
    index = np.argmax(prediction)
    return class_names[index].strip()
EOF && \
cat > utils/helpers.py << 'EOF'
# helpers.py

EOF && \
cat > main.py << 'EOF'
import RPi.GPIO as GPIO
import time
from config import TAPAS, CAP_MAX
from model.loader import load_model_and_labels
from model.predictor import predict_class
from hardware.camera import capture_image
from hardware.lcd_display import show_message
from hardware.movement import setup_motion_sensor, detect_motion
from hardware.servo import open_lid
from hardware.ultrasonic import measure_distance

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    setup_motion_sensor()
    for tapa in TAPAS.values():
        GPIO.setup(tapa['pin'], GPIO.OUT)
        GPIO.setup(tapa['trig'], GPIO.OUT)
        GPIO.setup(tapa['echo'], GPIO.IN)

def main():
    setup()
    model, class_names = load_model_and_labels()

    while True:
        if detect_motion():
            show_message("Capturando...", "")
            capture_image()
            show_message("Clasificando...", "")
            predicted_class = predict_class(model, class_names)

            if predicted_class in TAPAS:
                tapa = TAPAS[predicted_class]
                dist = measure_distance(tapa['trig'], tapa['echo'])
                if dist < CAP_MAX:
                    open_lid(tapa['pin'])
                    show_message(f"{tapa['nombre']} abierto", "")
                else:
                    show_message(f"{tapa['nombre']} lleno", "")
            else:
                show_message("Clase no", "reconocida")
        else:
            show_message("Esperando...", "")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()

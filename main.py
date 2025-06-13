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

def open_lid(pin):
    servo = GPIO.PWM(pin, 50)
    servo.start(0)
    servo.ChangeDutyCycle(7)  # Abrir
    time.sleep(2)
    servo.ChangeDutyCycle(2)  # Cerrar
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
    servo.stop()

from rpi_lcd import LCD
import time

lcd = LCD()

def show_message(line1="", line2="", delay=1):
    lcd.text(line1, 1)
    lcd.text(line2, 2)
    time.sleep(delay)
    lcd.clear()

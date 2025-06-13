from rpi_lcd import LCD
import time

lcd = LCD()

while True:
	lcd.text("hola mundo",1)
	lcd.text("adios mundo",2)
	time.sleep(1)
	lcd.clear()
	time.sleep(1)
	
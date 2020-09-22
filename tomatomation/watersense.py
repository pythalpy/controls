# External Module Imports
import RPi.GPIO as GPIO
import time

# Pin Definitions:
h2oPin = 14 #BCM Pin 14, Board Pin 8
pumpPin = 21 #BCM Pin 21, Board Pin 40
ledPin = 15 #BCM


# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(h2oPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
pwm = GPIO.PWM(ledPin, 100)


# Sensing
pwm.start(0)
print("Sensing Start!")
try:
	while 1:
	
		i = GPIO.input(h2oPin)
		if i == 1:
			print("Water Detected!")
			pwm.ChangeDutyCycle(100)
		else:
			print("No Water!")
			pwm.ChangeDutyCycle(0)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.cleanup()


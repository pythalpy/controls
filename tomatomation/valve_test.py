# External Module Imports
import RPi.GPIO as GPIO
import time
import sys

# Pin Definitions:
valvePin = 4 # BCM Pin 14, Board Pin 8

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(valvePin, GPIO.OUT, initial=GPIO.LOW)

time.sleep(2)

print("SETTING HIGH")
#GPIO.output(4, GPIO.HIGH)
valvePWM = GPIO.PWM(valvePin, 30)
valvePWM.ChangeDutyCycle(100)
time.sleep(3)

print("SETTING LOW")
#GPIO.output(4, GPIO.LOW)
valvePWM.ChangeDutyCycle(0)


print("DONE")
GPIO.cleanup()


# PWM Initialization (Pin, Frequency):

# ledPWM = GPIO.PWM(ledPin, 100)
# ledPWM.start(0)
# pumpPWM.start(0)
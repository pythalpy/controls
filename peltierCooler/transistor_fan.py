import RPi.GPIO as GPIO
import time
import sys
#import os

FAN_PIN = 21
WAIT_TIME = 1
PWM_FREQ = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.HIGH)

try:
    while 1:
        print('hello')


except(KeyboardInterrupt):
    print("Fan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()
    
#!/usr/bin/python
import sys
import Adafruit_DHT
#from time import gmtime, strftime
from datetime import datetime
import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library



DHT_PIN = 17 #BCM Numbering System
DHT_SENSOR = Adafruit_DHT.DHT11

# LED Control
GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.
                          # Can use GPIO.setmode(GPIO.BCM) instead to use 
                          # Broadcom SOC channel names.

GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 to output mode.
pwm = GPIO.PWM(12, 100)   # Initialize PWM on pwmPin 100Hz frequency

# main loop of program
print("\nPress Ctl C to quit \n")  # Print blank line before and after message.
dc=0                               # set dc variable to 0 for 0%
pwm.start(dc)                      # Start PWM with 0% duty cycle

# try:
#   while True:                      # Loop until Ctl C is pressed to stop.
#     for dc in range(0, 50, 1):    # Loop 0 to 100 stepping dc by 5 each loop
#       pwm.ChangeDutyCycle(dc)
#       time.sleep(.01)             # wait .05 seconds at current LED brightness
#       print(dc)
#     for dc in range(50, 0, -1):    # Loop 95 to 5 stepping dc down by 5 each loop
#       pwm.ChangeDutyCycle(dc)
#       time.sleep(0.05)             # wait .05 seconds at current LED brightness
#       print(dc)
def single_flash_led(sleep_time):
    duty_high = 10
    duty_low = 0

    pwm.ChangeDutyCycle(duty_high)
    time.sleep(sleep_time) 
    pwm.ChangeDutyCycle(duty_low)
    time.sleep(sleep_time)

def multi_flash_led(n_flashes, sleep_time):
    for _ in range (n_flashes):
        single_flash_led(sleep_time)
        
def flash_two_digit_number(number):
    numby = str(round(number))
    multi_flash_led(int(numby[0]),0.5)
    time.sleep(0.5)
    multi_flash_led(int(numby[1]),0.2)
    
flash_time=datetime.now()
try:
    while True:

        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        temperature_F = temperature*1.8+32
        current_time = datetime.now()
        timez = current_time.strftime("%d/%m/%y (%H:%M:%S)")
        print ('{3} Temp={0:0.1f}C / {2:0.1f}F Humidity={1:0.1f}%'.format(temperature, humidity, temperature_F, timez))
        time_since_last_flash = current_time - flash_time 
        
        if time_since_last_flash.total_seconds() > 30:
            flash_two_digit_number(temperature_F)
            flash_time=datetime.now()

            
        if humidity is not None and temperature is not None:
            print('{3} Temp={0:0.1f}C / {2:0.1f}F Humidity={1:0.1f}%'.format(temperature, humidity, temperature_F, timez))
        else:
            print("Failed to retrieve data from humidity sensor")

except KeyboardInterrupt:
  print("Ctl C pressed - ending program")

pwm.stop()                         # stop PWM
GPIO.cleanup()                     # resets GPIO ports used back to input mode

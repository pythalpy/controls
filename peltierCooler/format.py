#test format

a= 5.0068

print(a)
b='%.2f' % a
print(b)
c="{:.2f}".format(a)
print(c)
# #  MBTechWorks.com 2016
# #  Pulse Width Modulation (PWM) demo to cycle brightness of an LED
# 
# import RPi.GPIO as GPIO   # Import the GPIO library.
# import time               # Import time library
# 
# GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.
#                           # Can use GPIO.setmode(GPIO.BCM) instead to use 
#                           # Broadcom SOC channel names.
# 
# GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 to output mode.
# pwm = GPIO.PWM(12, 100)   # Initialize PWM on pwmPin 100Hz frequency

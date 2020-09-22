#  MBTechWorks.com 2016
#  Pulse Width Modulation (PWM) demo to cycle brightness of an LED

import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.
                          # Can use GPIO.setmode(GPIO.BCM) instead to use 
                          # Broadcom SOC channel names.

GPIO.setup(10, GPIO.OUT)  # Set GPIO pin 12 to output mode.
pwm = GPIO.PWM(10, 100)   # Initialize PWM on pwmPin 100Hz frequency

# main loop of program
print("\nPress Ctl C to quit \n")  # Print blank line before and after message.
dc=0                               # set dc variable to 0 for 0%
pwm.start(dc)                      # Start PWM with 0% duty cycle

try:
  while True:                      # Loop until Ctl C is pressed to stop.
    for dc in range(0, 100, 1):    # Loop 0 to 100 stepping dc by 5 each loop
      pwm.ChangeDutyCycle(dc)
      time.sleep(.05)             # wait .05 seconds at current LED brightness
      print(dc)
    time.sleep(5) 
    for dc in range(100, 0, -1):    # Loop 95 to 5 stepping dc down by 5 each loop
      pwm.ChangeDutyCycle(dc)
      time.sleep(0.05)             # wait .05 seconds at current LED brightness
      print(dc)
    time.sleep(5)

except KeyboardInterrupt:
  print("Ctl C pressed - ending program")

pwm.stop()                         # stop PWM
GPIO.cleanup()                     # resets GPIO ports used back to input mode

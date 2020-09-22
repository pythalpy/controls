# External Module Imports
import RPi.GPIO as GPIO
import time
import sys

# Pin Definitions:
h2oPin = 14 #BCM Pin 14, Board Pin 8
pumpPin = 21 #BCM Pin 21, Board Pin 40
ledPin = 15 #BCM

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(h2oPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(pumpPin, GPIO.OUT, initial=GPIO.LOW)

# PWM Initialization (Pin, Frequency):
pwm_pump = GPIO.PWM(pumpPin, 25)
pwm_led = GPIO.PWM(ledPin, 100)
pwm_led.start(0)
pwm_pump.start(0)

# Sensing
i=0


# Scheduler Time Check
current_time=time.localtime()
if current_time.tm_hour == 8:
    watering_time = True
else:
    watering_time = False

# Manually Enabling
watering_time = True
start_time = time.time()

print("Sensing Started on "+str(current_time.tm_mon) + "/" + str(current_time.tm_mday) + "at "  + str(current_time.tm_hour) + ":" + str(current_time.tm_min) + "!")
try:

    while watering_time:
        watering_complete = False
        #start_time = time.time()
        
        if time.time() - start_time < 30:
            pwm_pump.ChangeDutyCycle(100)
        else:
            i = GPIO.input(h2oPin)
            if i == 1:
                print("Water Detected! Pump Off")
                pwm_led.ChangeDutyCycle(100)
                pwm_pump.ChangeDutyCycle(0)
                end_time=time.time()
            elif time.time() - start_time > 60:
                print("Pump Time Maxed Out, Shutting Off Pump!")
                pwm_led.ChangeDutyCycle(0)
                pwm_pump.ChangeDutyCycle(0)
                end_time=time.time()
            else:
                print("No Water Detected. Continue Pumping")
                pwm_led.ChangeDutyCycle(0)
                pwm_pump.ChangeDutyCycle(100)
        time.sleep(1)
        print("Time Elapsed: ", time.time()-start_time)
        
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print("Program Interrupted By Keyboard")
    GPIO.cleanup()
    sys.exit()


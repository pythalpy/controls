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
pumpPWM = GPIO.PWM(pumpPin, 25)
ledPWM = GPIO.PWM(ledPin, 100)
ledPWM.start(0)
pumpPWM.start(0)

## Sensing
water_sense = 0 # Initial Water Sensor Value: False
running=True

w_time_hr = 8 # Manually Enabling Scheduler for Testing Purposes
watering_complete = False #initial value, may not be req'd
print("Scheduler Started On "+str(time.ctime())"!")

try:
    while running:
        # Scheduler Time Check
        c_time=time.localtime() #Get Current Time
        if c_time.tm_hour == w_time_hr:
            start_time = time.time()   
            pumpPWM.ChangeDutyCycle(100)
            ledPWM.ChangeDutyCycle(0)
            print("Starting Water Pump at "+str(time.ctime())"!")
            while watering_complete == False:
                water_sense = GPIO.input(h2oPin) # Check Water Sensor Status
                if (time.time() - start_time) > 30 and water_sense == 1: # Minimum Pump Runtime: 30 seconds and Sensor Check
                    pumpPWM.ChangeDutyCycle(0) # Shutoff Pump
                    ledPWM.ChangeDutyCycle(100) # Turn On Status LED   
                    watering_complete = True
                    end_time = time.time() # Capture End Time
                    total_duration = end_time - start_time
                    print("Water Detected! Pump Off")
                    print("Total Pumping Time = " + str(round(total_duration)) + " seconds")
                elif (time.time() - start_time) > 60:
                    pumpPWM.ChangeDutyCycle(0)
                    ledPWM.ChangeDutyCycle(100)
                    watering_complete = True
                    end_time=time.time()
                    total_duration = end_time - start_time
                    print("Pump Time Maxed Out, Shutting Off Pump!")  
                    print("Total Pumping Time = " + str(round(total_duration)) + " seconds")               
                else:
                    print("No Water Detected. Continue Pumping")
        else:
            time.sleep(5)
            print("It's not time to water yet. Watering scheduled for hour #" + w_time_hr + " of 24")
        
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print("Program Interrupted By Keyboard")
    running=False
    GPIO.cleanup()
    sys.exit()


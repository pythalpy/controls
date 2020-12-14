# External Module Imports
# import RPi.GPIO as GPIO
from RPI import GPIO
import time
import sys

# Pin Definitions:
h2oPin = 14 # BCM Pin 14, Board Pin 8
pumpPin = 21 # BCM Pin 21, Board Pin 40
ledPin = 15 # BCM
valvePin1 = 4
valvePin2 = 17

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(h2oPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(pumpPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valvePin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(valvePin2, GPIO.OUT, initial=GPIO.LOW)

# PWM Initialization (Pin, Frequency):
pumpPWM = GPIO.PWM(pumpPin, 25)
ledPWM = GPIO.PWM(ledPin, 100)
ledPWM.start(0)
pumpPWM.start(0)

# Sensing
water_sense = 0  # Initial Water Sensor Value: False
w_time_hr = 8  # Set Scheduler to Start at 8 AM
watering_complete = False  # initial value, may not be req'd
running = True

# Pump Actions


def start_pump():
    open_valve()
    time.sleep(2)
    pumpPWM.ChangeDutyCycle(100)
    print(str(time.ctime())+ ": " + "Starting Water Pump!")  


def stop_pump():
    close_valve()
    time.sleep(2)
    pumpPWM.ChangeDutyCycle(0) # Shutoff Pump
    ledPWM.ChangeDutyCycle(0) # Turn On Status LED   
    end_time = time.time() # Capture End Time
    total_duration = end_time - start_time
    print(str(time.ctime())+ ": " + "Total Pumping Time = " + str(round(total_duration)) + " seconds")


def open_valve():
    GPIO.output(valvePin1, GPIO.High) # +4.5V 30ms Pulse
    time.sleep(0.03)
    GPIO.output(valvePin1, GPIO.Low)

    
def close_valve():
    GPIO.output(valvePin2, GPIO.High) # -4.5V 30ms Pulse
    time.sleep(0.03)
    GPIO.output(valvePin2, GPIO.Low)


# LED Flashing
def single_flash_led(sleep_time):
    duty_high = 80
    duty_low = 0

    ledPWM.ChangeDutyCycle(duty_high)
    time.sleep(sleep_time) 
    ledPWM.ChangeDutyCycle(duty_low)
    time.sleep(sleep_time)


def multi_flash_led(n_flashes, sleep_time):
    for _ in range(n_flashes):
        single_flash_led(sleep_time)


try:
    while running:
        c_time=time.localtime()  # Get Current Time
        w_time_hr = c_time.tm_hour  # FORCE START FOR TESTING
        if c_time.tm_hour == w_time_hr:
            print(str(time.ctime()) + ": " + "Watering Started!")
            start_time = time.time()  
            start_pump()
            multi_flash_led(2, 0.1)
            while not watering_complete:
                water_sense = GPIO.input(h2oPin) # Check Water Sensor Status
                if (time.time() - start_time) > 3 and water_sense == 1:  # Minimum Pump Runtime: 3 seconds and Sensor Check
                    stop_pump()
                    watering_complete = True
                    print(str(time.ctime())+ ": " + "Water Detected! Pump Off")
                    multi_flash_led(4, 0.1)
                elif (time.time() - start_time) > 240: # 4 Minute Max Runtime
                    stop_pump()
                    watering_complete = True
                    print(str(time.ctime())+ ": " + "Pump Time Maxed Out, Shutting Off Pump!")
                    multi_flash_led(5, 0.1)             
                else:
                    print(str(time.ctime())+ ": " + "No Water Detected. Continue Pumping")
                    multi_flash_led(1, 0.1)
                    time.sleep(1)
            multi_flash_led(5, 1)
            time.sleep(3600)
        else:
            time.sleep(60)
            multi_flash_led(3, 1)
            print("It's not time to water yet. Watering scheduled for hour #" + w_time_hr + " of 24")

except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    print("Program Interrupted By Keyboard")
    stop_pump()
    running = False
    GPIO.cleanup()
    sys.exit()


#w_time_hr = c_time.tm_hour # FOR TESTING: ***Force Start NOW***

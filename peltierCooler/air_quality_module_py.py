# Raspberry Pi Adjustable Air Quality Detector Controlled via GUI
#
# Raspberry Pi 3B+
# 
# By Kutluhan Aktar
#
# Learn how to develop a GUI, named Air Quality Module, to control a mini pan-tilt kit and get information from an MQ-135 Air Quality Sensor.
# Also, you can change the background light (RGB) via the GUI.
# 
# Get more information on the project page:
# https://theamplituhedron.com/projects/Raspberry-Pi-Adjustable-Air-Quality-Detector-Controlled-via-GUI/


from guizero import App, Box, Text, TextBox, PushButton, ButtonGroup, MenuBar, info, yesno, warn
from time import sleep
from subprocess import call 
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


# Create the SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# Create the mcp object
mcp = MCP.MCP3008(spi, cs)

# Create analog inputs connected to the input pins on the MCP3008.
channel_0 = AnalogIn(mcp, MCP.P0)

# Define RGB pins settings and PWM frequencies
GPIO.setmode(GPIO.BCM)
red_pin = 2
green_pin = 3
blue_pin = 4
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
red_value = GPIO.PWM(red_pin, 100)
blue_value = GPIO.PWM(blue_pin, 100)
green_value = GPIO.PWM(green_pin, 100)
red_value.start(100)
blue_value.start(100)
green_value.start(100)

# Define servo motor pin settings and PWM frequencies
servo_base_pin = 20
servo_arm_pin = 21
GPIO.setup(servo_base_pin, GPIO.OUT)
GPIO.setup(servo_arm_pin, GPIO.OUT)
servo_base_value = GPIO.PWM(servo_base_pin, 50)
servo_arm_value = GPIO.PWM(servo_arm_pin, 50)
servo_base_value.start(0)
servo_arm_value.start(0)


# Define menu bar options' commands (functions).
def Tutorial():
    # Open the project page if requested.
    go_to_tutorial = yesno("Open Tutorial", "Get more information about the project!")
    if go_to_tutorial == True:
        command = "chromium-browser https://theamplituhedron.com/projects/"
        call([command], shell=True)
        print("Project Tutorial!")
    else:
        warn("Close", "Return to the application!")

def Components():
    info("Components", "Raspberry Pi 3B+\nMQ-135 Sensor\nMini Pan-Tilt Kit\n2 x Servo Motor\nRGB LED\n2 x Mini Breadboard\nMCP3008")
    
def About():
    info("About", "Develop a GUI, named Air Quality Module, to control a mini pan-tilt kit and get information from an MQ-135 Air Quality Sensor. Also, you can change the background light (RGB) on the GUI.")

#  Define application commands and features:
def _range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
def evaluateSensorValue():
    # Test your module, then define the value range - in this case between 0 and 60000.
    sensorValue = _range(channel_0.value, 0, 60000, 0, 1023)
    sensor_value.value = sensorValue
    # Threshold
    if(sensorValue > 300):
        status_text.value = "Status: DANGER"
        status_text.text_color = "yellow"
        warn("!!!DANGER!!!", "Air Quality Deteriorating!")
    else:
        status_text.value = "Status: OK"
        status_text.text_color = "green"
    
def adjust_color():
    red = _range(int(r_input.value), 0, 255, 1, 100)
    green = _range(int(g_input.value), 0, 255, 1, 100)
    blue = _range(int(b_input.value), 0, 255, 1, 100)
    red_value.ChangeDutyCycle(101 - red)
    blue_value.ChangeDutyCycle(101 - blue)
    green_value.ChangeDutyCycle(101 - green)
    
def base_tilt_move():
    # Cycle values between 2 and 12 are working precisely:
    selected_angle = 2 + (int(base_angle.value) / 18)
    servo_base_value.ChangeDutyCycle(selected_angle)
    sleep(0.5)
    servo_base_value.ChangeDutyCycle(0)

def arm_tilt_move():
    selected_angle = 2 + (int(arm_angle.value) / 18)
    servo_arm_value.ChangeDutyCycle(selected_angle)
    sleep(0.5)
    servo_arm_value.ChangeDutyCycle(0)
    
# Create the GUI application.
appWidth = 1200
appHeight = 500
app = App(title="Air Quality Module", bg="#eb2e00", width=appWidth, height=appHeight)
# Define menu bar options.
menubar = MenuBar(app, toplevel=["Tutorial", "Components", "About"],
                  options=[
                      [ ["View", Tutorial] ],
                      [ ["Inspect", Components ] ],
                      [ ["About", About] ]
                  ])
# Design the interface using the box widget.
top = Box(app, width="fill", height=appHeight / 2, align="top")
bottom = Box(app, width="fill", height=appHeight / 2, align="bottom")
color_interface = Box(top, width=appWidth / 2, align="left", layout="grid", border=True)
quality_interface = Box(top, width=appWidth / 2, align="right")
base_interface = Box(bottom, width=appWidth / 2, align="left")
arm_interface = Box(bottom, width=appWidth / 2, align="right")

# RGB Color Interface
color_header = Text(color_interface, text="Adjust RGB Background Color", color="#002699", size=20, grid=[0,0])
r_label = Text(color_interface, text="R :", color="#1a53ff", size=15, grid=[0,1])
r_input = TextBox(color_interface, grid=[1,1])
r_input.bg = "#ff5c33"
r_input.text_color = "#1a53ff"
g_label = Text(color_interface, text="G :", color="#1a53ff", size=15, grid=[0,2])
g_input = TextBox(color_interface, grid=[1,2])
g_input.bg = "#ff5c33"
g_input.text_color = "#1a53ff"
b_label = Text(color_interface, text="B :", color="#1a53ff", size=15, grid=[0,3])
b_input = TextBox(color_interface, grid=[1,3])
b_input.bg = "#ff5c33"
b_input.text_color = "#1a53ff"
adjust_button = PushButton(color_interface, grid=[2,4], width="20", text="Adjust", command=adjust_color)
adjust_button.bg = "#002699"
adjust_button.text_color = "white"

# Air Quality Interface
quality_header = Text(quality_interface, text="Air Quality Sensor", color="#002699", size=20, align="top")
sensor_value = Text(quality_interface, text="TEST", color="#002699", size=120)
status_text = Text(quality_interface, text="Status: OK", color="green", size=15, align="bottom")
# Update the sensor value.
sensor_value.repeat(1000, evaluateSensorValue)

# Mini Pan-Tilt Base Interface
base_header = Text(base_interface, text="Pan-Tilt Base", color="#002699", size=20)
base_angle = ButtonGroup(base_interface, options=["0", "30", "45", "90", "135", "180"], selected="0", width=20, command=base_tilt_move)
base_angle.text_size = 15
base_angle.text_color = "white"

# Mini Pan-Tilt Arm Interface
arm_header = Text(arm_interface, text="Pan-Tilt Arm", color="#002699", size=20)
arm_angle = ButtonGroup(arm_interface, options=["0", "30", "45", "90", "135", "180"], selected="0", width=20, command=arm_tilt_move)
arm_angle.text_size = 15
arm_angle.text_color = "white"

# Start the loop.
app.display()
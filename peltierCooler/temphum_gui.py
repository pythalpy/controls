from guizero import App, PushButton, Slider, Text
import sys
import Adafruit_DHT
import threading
from datetime import datetime
import time
DHT_PIN = 17 #BCM Numbering System
DHT_SENSOR = Adafruit_DHT.DHT11

current_time = datetime.now()
timez = current_time.strftime("%d/%m/%y (%H:%M:%S)")

# Action I would like to perform
def read_sensor():
    # Capturing the sensor data
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    temperature_F = temperature*1.8+32   
    #temp_text.value='%.1f' % temperature_F+ " F"
    temp_text.value="{:.1f}".format(temperature_F)+" F"
    #hum_text.value='%.0f' % humidity + " %"
    hum_text.value="{:.0f}".format(humidity)+" %"
    current_time = datetime.now()
    timez = current_time.strftime("%H:%M:%S")
    time_text.value=timez
    print ('{3} Temp={0:0.1f}C / {2:0.1f}F Humidity={1:0.1f}%'.format(temperature, humidity, temperature_F, timez))

#c="{:.2f}".format(a)

# GUIZERO DISPLAY
from guizero import App, PushButton, Slider, Text

app = App(title="Peltier Cooler Temp Monitor", width=500, height = 300)

time_label = Text(app, text="The time is:")
time_text = Text(app, text="-", size = 20)

temp_label = Text(app, text="The current temperature is:")
temp_text = Text(app, text="-", size = 40, color="blue")

hum_label = Text(app, text="The current Humidity is:")
hum_text = Text(app, text="-", size = 40, color="orange")
temp_text.repeat(5000, read_sensor)


designby_text = Text(app, text="Jaanisar - Pythalpy Engineering", align='bottom', size = 8)
app.display()
            
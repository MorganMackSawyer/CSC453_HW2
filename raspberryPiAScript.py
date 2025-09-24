#!python3
import paho.mqtt.client as mqtt
import time
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

TOPIC_STATUS = "Status/RaspberryPiA"
TOPIC_LIGHTSENSOR = "lightSensor"
TOPIC_THRESHOLD = "threshold"

#Define MCP3008 Port Numbers
potPORT = 7
ldrPORT = 0

# Setup SPI and MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP3008(spi, cs)

# Create channels (LDR on 0, Pot on 1 - adjust as needed)
ldr = AnalogIn(mcp, potPORT)
pot = AnalogIn(mcp, ldrPORT)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.publish(TOPIC_STATUS, "online", qos=2, retain=True)
    else:
        print("Bad connection Returned code = ", rc)

def on_disconnect(client, userdata, flags, rc=0):
    client.publish(TOPIC_STATUS, "offline", qos=2, retain=True)

# Use this call back function on computer #2 to display recieved time
def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("message received", m_decode)


broker = '172.20.10.3'
port = 1883
client = mqtt.Client("RaspberryPiA")
client.on_connect = on_connect # call back function
client.on_disconnect = on_disconnect
client.on_message = on_message


client.connect(broker, port)
client.loop_start()
client.subscribe(TOPIC_LIGHTSENSOR)
client.subscribe(TOPIC_THRESHOLD)
time.sleep(2)

while 1:
    # Read LDR
    ldr_value = ldr.value
    ldr_voltage = ldr.voltage

    # Read potentiometer  
    pot_value = pot.value
    pot_voltage = pot.voltage

    # Print results
    print(f"LDR: {ldr_value} | {ldr_voltage:.2f}V | POT: {pot_value} | {pot_voltage:.2f}V")
    

    time.sleep(100)  # Wait 1 second
    client.loop_stop()
    client.disconnect()
    break

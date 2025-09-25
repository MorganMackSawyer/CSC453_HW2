#!python3
import paho.mqtt.client as mqtt
import sys
import time
import threading
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

def normalize_pot(value):
    pot_min = 10000
    pot_max = 60000
    return max(0.0, min(1.0, (value - pot_min) / (pot_max - pot_min)))

def normalize_ldr(value):
    ldr_min = 60
    ldr_max = 300
    return max(0.0, min(1.0, (value - ldr_min) / (ldr_max - ldr_min)))

#Define MCP3008 Port Numbers
potPORT = 7
ldrPORT = 0

# Setup SPI and MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP3008(spi, cs)

# Create channels (LDR on 0, Pot on 1 - adjust as needed)
ldr = AnalogIn(mcp, ldrPORT)
pot = AnalogIn(mcp, potPORT)
TOPIC_STATUS = "Status/RaspberryPiA"
TOPIC_LIGHTSENSOR = "lightSensor"
TOPIC_THRESHOLD = "threshold"

def pollSensors(ldr, pot):
    i = 0
    while 1:
        # Read LDR
        ldr_value = ldr.value
        
        # Read potentiometer  
        pot_value = pot.value
        
        # Print results
        norm_ldr_val = normalize_ldr(ldr_value)
        norm_pot_val = normalize_pot(pot_value)
        i = i + 1


        time.sleep(0.1) #100 ms
            

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(TOPIC_LIGHTSENSOR)
        client.subscribe(TOPIC_THRESHOLD)
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


thread1 = threading.Thread(target=pollSensors, args=(ldr, pot))
thread1.daemon = True
thread1.start()

broker = '172.20.10.3'
port = 1883
client = mqtt.Client("RaspberryPiA")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.will_set(
    topic="Status/RaspberryPiA",
    payload="offline",
    qos=2,
    retain=True
)

client.connect(broker, port)
client.loop_start()
time.sleep(1)

try:
    while 1:
        user_input = input("")
        print('hi')
        if "Quit" == user_input:
            client.loop_stop()
            sys.exit(0)

except KeyboardInterrupt:
    client.publish(TOPIC_STATUS, "offline", qos=2, retain=True)


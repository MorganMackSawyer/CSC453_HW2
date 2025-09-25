#!python3
import paho.mqtt.client as mqtt
import time
import logging
import os

file_path = 'app.log'  # Replace with the actual file path

if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File '{file_path}' successfully deleted.")
else:
    print(f"File '{file_path}' does not exist.")

TURN_ON = "TurnOn"
TURN_OFF = "TurnOff"
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')
start_time = time.strftime("%H:%M:%S", time.localtime()) 

def on_connect(client, userdata, flags, rc):
    client.subscribe("lightSensor")
    client.subscribe("threshold")
    client.subscribe("LightStatus")
    client.subscribe("Status/RaspberryPiA")
    client.subscribe("Status/RaspberryPiC")
    global start_time 
    start_time = time.strftime("%H:%M:%S", time.localtime()) 

    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection Returned code = ", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, msg):
    global start_time
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))

    if TURN_ON == m_decode:
        end_time = time.strftime("%H:%M:%S", time.localtime()) 
        logging.info("LED1 was OFF from " + start_time + " - " + end_time)
        start_time = end_time
    elif TURN_OFF == m_decode:
        end_time = time.strftime("%H:%M:%S", time.localtime()) 
        logging.info("LED1 was ON from " + start_time + " to " + end_time)
        start_time = end_time
    print(time.strftime("%H:%M:%S", time.localtime()) + ": " + topic + ": ", m_decode)


broker = '172.20.10.3'
port = 1883
client = mqtt.Client("Laptop2")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(broker, port)
time.sleep(2)
try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()


#!python3
import paho.mqtt.client as mqtt
import time
import logging

TURN_ON = "TurnOn"
TURN_OFF = "TurnOff"
logging.basicConfig(level=logging.INFO, format='%(message)s')
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

    if TURN_ON == topic:
        end_time = time.strftime("%H:%M:%S", time.localtime()) 
        logging.info("LED1 was OFF from " + start_time + " - " + end_time)
        start_time = end_time
    elif TURN_OFF == topic:
        end_time = time.strftime("%H:%M:%S", time.localtime()) 
        logging.info("LED1 was ON from " + start_time + " to " + end_time)
        start_time = end_time
    print(time.strftime("%H:%M:%S", time.localtime()) + " - message received:", m_decode)


broker = '172.20.10.3'
port = 1883
client = mqtt.Client("Laptop2")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(broker, port)
time.sleep(2)
client.loop_forever

while 1:
    user_input = input("")
    client.publish("LightStatus", user_input)
    if "Quit" == user_input:
        client.loop_stop()
        client.disconnect()
        break


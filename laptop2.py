#!python3
import socket
import sys
import threading
import paho.mqtt.client as mqtt
import time
import random

def on_log(client, userdata, level, buf):
    print("log: " + buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection Returned code = ", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("message received", m_decode)

# Public IP 152.7.255.207
# Ip address 127.0.0.1
broker = '127.0.0.1'
port = 1883
client = mqtt.Client("Test_User")

client.on_connect = on_connect # call back function
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message

client.connect(broker, port)
client.loop_start()
client.subscribe("lightSensor")
client.subscribe("threshold")
client.subscribe("LightStatus")
client.subscribe("Status/RaspberryPiA")
client.subscribe("Status/RaspberryPiC")
client.publish("breadboard/sensor", "my first message", qos=2, retain=True)
time.sleep(2)

while 1:
    user_input = input("")
    if "Quit" == user_input:
        client.loop_stop()
        client.disconnect()
        break


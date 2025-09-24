#!python3
import paho.mqtt.client as mqtt
import time

TOPIC_STATUS = "Status/RaspberryPiA"
TOPIC_LIGHTSENSOR = "lightSensor"
TOPIC_THRESHOLD = "threshold"

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
    user_input = input("")
    if "Quit" == user_input:
        client.loop_stop()
        client.disconnect()
        break

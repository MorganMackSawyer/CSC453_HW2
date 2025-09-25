import paho.mqtt.client as mqtt
import logging
import sys
import time
# fill in to update the server ip address
hostname = "172.20.10.3"
lightSensorValue = -1.0
ldrValue = -1.0
lastSentStatus = False
TOPIC_STATUS = "Status/RaspberryPiC"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    LightStatus = client.subscribe("lightSensor", 2)
    Threshold = client.subscribe("threshold", 2)
    client.subscribe("LightStatus", 2)
    client.publish(TOPIC_STATUS, "online", qos=2, retain=True)

def wait_for(client,msgType,period=0.25):
  if msgType=="SUBACK":
    if client.on_subscribe:
      while not client.suback_flag:
        logging.info("waiting suback")
        client.loop()  #check for messages
        time.sleep(period)

def on_message(client, userdata, message):
  global lightSensorValue
  global ldrValue
  global lastSentStatus
  print("message received  ",str(message.payload.decode("utf-8")),\
          "topic",message.topic,"retained ",message.retain)
  message_str = str(message.payload.decode("utf-8"))
  if message.topic == "lightSensor":
    lightSensorValue = float(message_str)
  if message.topic == "threshold":
    ldrValue = float(message_str)
  if message.topic == "lightSensor" or message.topic == "threshold":
    flag = lightSensorValue <= ldrValue

    if flag and flag != lastSentStatus:
      client.publish("LightStatus", "TurnOn", qos=2, retain=True)
    elif not flag and flag != lastSentStatus:
      client.publish("LightStatus", "TurnOff", qos=2, retain=True)


  if message.topic == "LightStatus":
    if message_str == "TurnOff":
      lastSentStatus = False
    elif message_str == "TurnOn":
      lastSentStatus = True


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(hostname, 1883, 60)
client.loop_start()
time.sleep(1)

try:
    while 1:
        user_input = input("")
        if "Quit" == user_input:
          client.publish(TOPIC_STATUS, "offline", qos=2, retain=True)
          client.publish("LightStatus", "TurnOff", qos=2, retain=True)
          sys.exit(0)
except KeyboardInterrupt:
    client.publish(TOPIC_STATUS, "offline", qos=2, retain=True)
    client.publish("LightStatus", "TurnOff", qos=2, retain=True)

finally:
  client.loop_stop()
  sys.exit(1)
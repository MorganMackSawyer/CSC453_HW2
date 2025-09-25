import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import sys

# fill in to update the server ip address
hostname = "172.20.10.3"
LightStatus = "None"
LED1 = 17
LED2 = 18
LED3 = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    LightStatus = client.subscribe("LightStatus", 2)
    PiAStatus = client.subscribe("Status/RaspberryPiA", 2)
    PiCStatus = client.subscribe("Status/RaspberryPiC", 2)
def wait_for(client,msgType,period=0.25):
  if msgType=="SUBACK":
    if client.on_subscribe:
      while not client.suback_flag:
        logging.info("waiting suback")
        client.loop()  #check for messages
        time.sleep(period)
        
def on_disconnect(client, userdata, flags, rc=0):
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(LED3, False)

def on_message(client, userdata, message):
    global LightStatus
    print("message received  ",str(message.payload.decode("utf-8")),\
          "topic",message.topic,"retained ",message.retain)
    message_str = str(message.payload.decode("utf-8"))
    if message.topic  == "LightStatus":
      LightStatus = message
      if message_str == "TurnOn":
        # turn on led 1
        GPIO.output(LED1, True)
        print("Turn on led 1")
      if message_str == "TurnOff":
        # turn off led 1
        GPIO.output(LED1, False)
        print("turn off led 1") 


    if message.topic == "Status/RaspberryPiA":
      if message_str == "online":
        # turn on led 2
        GPIO.output(LED2, True)
        print("Turn on led 2")

      if message_str == "offline":
        # turn off led 2
        GPIO.output(LED2, False)
        print("turn off led 2") 
    
    if message.topic == "Status/RaspberryPiC":
      if message_str == "online":
        GPIO.output(LED3, True)
        print("turn on led 3")   
        if LightStatus == "TurnOn":
          GPIO.output(LED1, True)
          print("turn on led 1")
        if LightStatus == "TurnOff":
          GPIO.output(LED1, False)
          print("turn off led 1")

      if message_str == "offline":
        GPIO.output(LED1, False)
        GPIO.output(LED3, False)
        print("turn off led 1 and 3")
      
    if message.retain==1:
        print("This is a retained message " + message_str)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
time.sleep(2)


try:
  client.connect(hostname, 1883, 60)

except Exception as e:
  logging.info("Error on subscribe " + e)
  client.loop_stop()
  sys.exit(1)
try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(LED3, False)

  

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# fill in to update the server ip address
broker = ("172.0.0.0", 1883, 60)
LightStatus = "None"
LED1 = 17
LED2 = 18
LED3 = 22
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

def on_message(client, userdata, message):
    print("message received  ",str(message.payload.decode("utf-8")),\
          "topic",message.topic,"retained ",message.retain)
    message = str(message.payload.decode("utf-8"))
    if message.topic  == "LightStatus":
      LightStatus = message
      if message == "TurnOn":
        # turn on led 1
        GPIO.output(LED1, True)
        print("Turn on led 1")
      if message == "TurnOff":
        # turn off led 1
        GPIO.output(LED1, False)
        print("turn off led 1") 


    if message.topic == "Status/RaspberryPiA":
      if message == "online":
        # turn on led 2
        GPIO.output(LED2, True)
        print("Turn on led 2")

      if message == "offline":
        # turn off led 2
        GPIO.output(LED2, False)
        print("turn off led 2") 
    
    if message.topic == "Status/RaspberryPiC":
      if message == "online":
        GPIO.output(LED3, True)
        print("turn on led 3")   
        if LightStatus == "TurnOn":
          GPIO.output(LED1, True)
          print("turn on led 1")
        if LightStatus == "TurnOff":
          GPIO.output(LED1, False)
          print("turn off led 1")

      if message == "offline":
        GPIO.output(LED1, False)
        GPIO.output(LED3, False)
        print("turn off led 1 and 3")
      
    if message.retain==1:
        print("This is a retained message")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

try:
  client.connect(broker)

except Exception as e:
  logging.info("Error on subscribe " + e)
  client.loop_stop()
  sys_exit(1)

client.loop_forever()
  

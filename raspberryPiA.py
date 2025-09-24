#!python3
import socket
import sys
import threading
import paho.mqtt.client as mqtt
import time
import random

TOPIC_STATUS = "Status/RaspberryPiA"

def on_log(client, userdata, level, buf):
    print("log: " + buf)

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
client.on_log = on_log
client.on_message = on_message


client.connect(broker, port)
client.loop_start()
client.subscribe("lightSensor")
client.subscribe("threshold")
client.publish("breadboard/sensor", "my first message", qos=2, retain=True)
time.sleep(2)

while 1:
    user_input = input("")
    if "Quit" == user_input:
        client.loop_stop()
        client.disconnect()
        break

# # --- Connection Settings ---
# broker = 'localhost'  # Replace with your Mosquitto broker's IP address if not local
# port = 1883
# topic = "test/topic"
# client_id = f'python-mqtt-{random.randint(0, 1000)}'


# # --- Callback functions ---
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected to MQTT Broker!")
#         client.subscribe(topic)
#     else:
#         print('Failed to connect, return code %d\n', rc)

# def on_message(client, userdata, msg):
#     print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# # --- MQTT Client Setup ---
# client = mqtt_client.Client(client_id)
# client.on_connect = on_connect
# client.on_message = on_message

# # --- Connect and Start Loop ---
# client.connect(broker, port)

# # --- Publish messages ---
# def publish_message(message):
#     result = client.publish(topic, message)
#     status = result[0]
#     if status == 0:
#         print(f"Sent `{message}` to topic `{topic}`")
#     else:
#         print(f"Failed to send message to topic {topic}")

# # Start the network loop
# client.loop_forever()


# HOST = ''
# PORT = 9001
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Socket Created")
# try:

#     s.bind((HOST, PORT))
# except socket.error:
#     print("Bind failed. Error Code: " + str(socket.error))
#     sys.exit()
# print("Socket bind complete")
# s.listen(10)
# print("Socket now listening")

# #Tread handling
# def client_thread(conn):
#     conn.send("Welcome to the server.\n")
#     while True:
#         data = conn.revc(1024)
#         reply = "Received: " + data
#         if not data:
#             break
#         conn.sendall(reply)
#     conn.close()

# while 1:
#     #wait to accept a connection - blocking call
#     conn, addr = s.accept()
#     print("Connected with " + addr[0] + ":" + str(addr[1]))
#     threading.Thread(target=client_thread, args=(conn,))
# s.close()

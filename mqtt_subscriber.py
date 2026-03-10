import paho.mqtt.client as mqtt
import json

# Broker details
BROKER = "10.35.24.93"
PORT = 1883
TOPIC = "irrigation/ESP001/sensors"

# When connected
def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)
    client.subscribe(TOPIC)

# When message received
def on_message(client, userdata, msg):
    print("\nRaw Message:", msg.payload.decode())

    try:
        data = json.loads(msg.payload.decode())
        print("Temperature:", data["temperature"])
        print("Humidity:", data["humidity"])
        print("Soil:", data["soil"])
        print("Distance:", data["distance"])
    except Exception as e:
        print("JSON Parse Error:", e)

# Create client
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Waiting for messages...")
client.loop_forever()

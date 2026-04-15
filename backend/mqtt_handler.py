import json
import paho.mqtt.client as mqtt
from config import BASE_TOPIC
from db_handler import save_sensor_data

mqtt_client = mqtt.Client()

def start_mqtt():
    mqtt_client.connect("127.0.0.1", 1883, 60)
    mqtt_client.loop_start()

    
def on_connect(client, userdata, flags, rc):
    print("Connected:", rc)

    topic = f"{BASE_TOPIC}/+/+/sensors"
    client.subscribe(topic)

    print("Subscribed to:", topic)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        topic_parts = msg.topic.split("/")
        user_id = int(topic_parts[1])
        plant_id = int(topic_parts[2])

        data["user_id"] = user_id
        data["plant_id"] = plant_id

        # ONLY SAVE DATA ✅
        save_sensor_data(data)

    except Exception as e:
        print("Error:", e)


def send_command(user_id, plant_id, water):
    topic = f"{BASE_TOPIC}/{user_id}/{plant_id}/command"

    payload = json.dumps({"plant_id": plant_id, "water": int(water)})  # ensure integer

    mqtt_client.publish(topic, payload)

    print("Command sent:", payload)

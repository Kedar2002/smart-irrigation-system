import sqlite3
import json
import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler

BROKER = "127.0.0.1"
PORT = 1883

SENSOR_TOPIC = "irrigation/ESP001/sensors"
COMMAND_TOPIC = "irrigation/ESP001/command"

DB_FILE = "sensor_data.db"


def init_db():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            soil INTEGER,
            distance REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


def save_sensor_data(data):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data (temperature, humidity, soil, distance)
        VALUES (?, ?, ?, ?)
    """,
        (
            data.get("temperature"),
            data.get("humidity"),
            data.get("soil"),
            data.get("distance"),
        ),
    )

    conn.commit()
    conn.close()

    print("Saved to DB")


def send_irrigation_command():

    payload = {"water": 200}

    message = json.dumps(payload)

    mqtt_client.publish(COMMAND_TOPIC, message)

    print("Irrigation command sent:", message)


def on_connect(client, userdata, flags, rc):

    print("Connected to MQTT Broker:", rc)

    client.subscribe(SENSOR_TOPIC)

    print("Subscribed to:", SENSOR_TOPIC)


def on_message(client, userdata, msg):

    payload = msg.payload.decode()

    print("\nReceived MQTT message:")
    print(payload)

    try:

        data = json.loads(payload)

        save_sensor_data(data)

    except Exception as e:

        print("JSON parse error:", e)


mqtt_client = mqtt.Client()

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def main():

    init_db()

    mqtt_client.connect(BROKER, PORT, 60)

    mqtt_client.loop_start()

    print("MQTT listener running...")

    # Scheduler
    scheduler = BackgroundScheduler()

    scheduler.add_job(send_irrigation_command, "interval", seconds=30)

    scheduler.start()

    print("Scheduler started: irrigation every 30 seconds")

    # keep program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    main()

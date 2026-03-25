import sqlite3
import json
import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler

BROKER = "127.0.0.1"
PORT = 1883

SENSOR_TOPIC = "irrigation/ESP001/sensors"
COMMAND_TOPIC = "irrigation/ESP001/command"

PROFILES_DB = "profiles.db"
SENSOR_DATA_DB = "sensor_data_v1.db"
PLANT_DB = "plants.db"
PROFILES = "profiles"
SENSOR_DATA = "sensor_data_v1"
PLANTS = "plants"


def init_profiles_db():
    conn = sqlite3.connect(PROFILES_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {PROFILES} (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    """
    )

    conn.commit()
    conn.close()


def init_sensor_db():

    conn = sqlite3.connect(SENSOR_DATA_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {SENSOR_DATA} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER,
            temperature REAL,
            humidity REAL,
            soil INTEGER,
            distance REAL,
            irrigation_status INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (plant_id) REFERENCES plants(plant_id)
        )
    """
    )

    conn.commit()
    conn.close()


def init_plants_db():
    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {PLANTS} (
            plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plant_name TEXT,
            plant_type TEXT,
            plant_age INTEGER,
            plant_height REAL,
            pot_type TEXT,
            pot_size REAL,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id) REFERENCES profiles(user_id)
        )
    """
    )

    conn.commit()
    conn.close()


def save_sensor_data(data):

    conn = sqlite3.connect(SENSOR_DATA_DB)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data_v1 (temperature, humidity, soil, distance, irrigation_status)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            data.get("temperature"),
            data.get("humidity"),
            data.get("soil"),
            data.get("distance"),
            data.get("irrigation_status"),
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

    init_profiles_db()
    init_sensor_db()
    init_plants_db()

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

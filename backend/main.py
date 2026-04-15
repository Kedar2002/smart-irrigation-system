import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from ml_model import predict_water
from mqtt_handler import mqtt_client, on_connect, on_message, send_command, start_mqtt
from config import BROKER, PORT
from db_handler import (
    init_profiles_db,
    init_sensor_db,
    init_plants_db,
    update_plant_dynamic_fields,
    get_plants_for_watering,
    log_irrigation_event,
    get_latest_data_with_plant,
    get_plants_schedule,
)
from irrigation_logic import decide_irrigation

scheduler = BackgroundScheduler()

# -------------------------------
# SCHEDULER JOBS
# -------------------------------

last_run = {}


def trigger_irrigation(plant_id, user_id, mode="manual_ml"):

    data = get_latest_data_with_plant(plant_id)

    if not data:
        print(f"⚠️ No data for plant {plant_id}")
        return None

    water, status = decide_irrigation(data)

    if status == 0 or water is None or water <= 0:
        print(f"❌ No irrigation needed for plant {plant_id}")
        return None

    send_command(user_id, plant_id, water)
    log_irrigation_event(plant_id, water, mode)

    print(f"✅ Irrigation triggered → Plant {plant_id}: {water}")

    return water


def schedule_all_plants():
    for job in scheduler.get_jobs():
        if job.id.startswith("plant_"):
            scheduler.remove_job(job.id)

    plants = get_plants_schedule()

    for plant in plants:
        plant_id = plant["plant_id"]
        user_id = plant["user_id"]
        watering_time = plant.get("watering_time")

        if not watering_time:
            continue

        hour, minute = map(int, watering_time.split(":"))

        scheduler.add_job(
            trigger_irrigation,
            "cron",
            hour=hour,
            minute=minute,
            args=[plant_id, user_id, "scheduled_ml"],
            id=f"plant_{plant_id}",
            replace_existing=True,
        )

        print(f"⏰ Scheduled Plant {plant_id} at {watering_time}")


def run_scheduler():
    scheduler.start()

    # ✅ Load schedules from DB
    schedule_all_plants()

    scheduler.add_job(update_plant_dynamic_fields, "interval", hours=1)

    print("Scheduler started...")


def main():
    # Init DBs
    init_profiles_db()
    init_sensor_db()
    init_plants_db()

    # Start scheduler in separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # MQTT setup
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    start_mqtt()
    mqtt_client.connect(BROKER, PORT, 60)

    print("System running...")
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()

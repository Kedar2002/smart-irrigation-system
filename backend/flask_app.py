from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3

from db_handler import (
    get_plants_by_user,
    get_plant_by_id,
    get_latest_sensor_data,
    get_irrigation_history_by_user,
    log_irrigation_event,
    get_latest_data_with_plant,
)
from irrigation_logic import decide_irrigation

from mqtt_handler import send_command, start_mqtt
from main import trigger_irrigation, schedule_all_plants

start_mqtt()

from config import (
    PROFILES_DB,
    PLANT_DB,
    PROFILES,
    PLANTS,
)

app = Flask(__name__)


def get_current_season():
    month = datetime.now().month

    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Winter"


# =====================================
# 🌱 PLANT APIs
# =====================================


# CREATE PLANT
@app.route("/plant/new", methods=["POST"])
def create_plant():
    data = request.get_json()
    season = get_current_season()
    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        INSERT INTO {PLANTS}
        (user_id, plant_name, plant_type, planter_type, plant_age, pot_size, season, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data.get("user_id"),
            data.get("plant_name"),
            data.get("plant_type"),
            data.get("planter_type"),
            data.get("plant_age"),
            data.get("pot_size"),
            season,
            data.get("notes"),
        ),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Plant added successfully"}), 201


# UPDATE PLANT
@app.route("/plant/<int:plant_id>", methods=["PUT"])
def update_plant(plant_id):
    data = request.get_json()

    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        UPDATE {PLANTS}
        SET plant_name = ?, plant_type = ?, planter_type = ?, plant_age = ?, pot_size = ?, notes = ?
        WHERE plant_id = ?
    """,
        (
            data.get("plant_name"),
            data.get("plant_type"),
            data.get("planter_type"),
            data.get("plant_age"),
            data.get("pot_size"),
            data.get("notes"),
            plant_id,
        ),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Plant updated"})


# DELETE PLANT
@app.route("/plant/<int:plant_id>", methods=["DELETE"])
def delete_plant(plant_id):
    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {PLANTS} WHERE plant_id = ?", (plant_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Plant deleted"})


# GET ALL PLANTS (uses db_handler)
@app.route("/plants/<int:user_id>", methods=["GET"])
def get_plants(user_id):
    return jsonify(get_plants_by_user(user_id))


# GET SINGLE PLANT (uses db_handler)
@app.route("/plant/<int:plant_id>", methods=["GET"])
def get_plant(plant_id):
    plant = get_plant_by_id(plant_id)
    if not plant:
        return jsonify({"error": "not found"}), 404
    return jsonify(plant)


# =====================================
# 👤 PROFILE / AUTH APIs
# =====================================


# CREATE PROFILE (Signup)
@app.route("/profile/new", methods=["POST"])
def create_profile():
    data = request.get_json()

    conn = sqlite3.connect(PROFILES_DB)
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            INSERT INTO {PROFILES} (username, email, password)
            VALUES (?, ?, ?)
        """,
            (data.get("username"), data.get("email"), data.get("password")),
        )
        conn.commit()
        return jsonify({"message": "Profile created successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

    finally:
        conn.close()


# LOGIN
@app.route("/login", methods=["POST"])
def login_profile():
    data = request.get_json()

    conn = sqlite3.connect(PROFILES_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    user = cursor.execute(
        f"""
        SELECT * FROM {PROFILES}
        WHERE username = ? AND password = ?
    """,
        (data.get("username"), data.get("password")),
    ).fetchone()

    conn.close()

    if user:
        return jsonify(
            {
                "message": "Login successful",
                "user_id": user["user_id"],
                "username": user["username"],
            }
        )
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# =====================================
# 📊 SENSOR DATA API
# =====================================


@app.route("/data", methods=["GET"])
def get_data():
    data = get_latest_sensor_data()
    if not data:
        return jsonify({"error": "no data"}), 404
    return jsonify(dict(data))


# =====================================
# 💧 IRRIGATION APIs
# =====================================


# MANUAL IRRIGATION
@app.route("/irrigation/manual", methods=["POST"])
def manual_irrigation():
    data = request.get_json()

    plant_id = data.get("plant_id")
    user_id = data.get("user_id")

    if plant_id is None or user_id is None:
        return jsonify({"error": "plant_id and user_id required"}), 400

    full_data = get_latest_data_with_plant(plant_id)

    if not full_data:
        return jsonify({"error": "No data available"}), 400

    water, status = decide_irrigation(full_data)

    if not water or water <= 0:
        return jsonify({"message": "No irrigation needed"})

    send_command(user_id, plant_id, water)
    log_irrigation_event(plant_id, water, "manual_ml")

    return jsonify(
        {"message": "Irrigation started", "plant_id": plant_id, "water": water}
    )


# IRRIGATION HISTORY
@app.route("/irrigation/history/<int:user_id>", methods=["GET"])
def irrigation_history(user_id):
    history = get_irrigation_history_by_user(user_id)
    return jsonify({"user_id": user_id, "history": history})


@app.route("/plant/watering-time", methods=["POST"])
def set_watering_time():
    data = request.get_json()

    plant_id = data.get("plant_id")
    time = data.get("time")  # format "HH:MM"

    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        UPDATE {PLANTS}
        SET watering_time = ?
        WHERE plant_id = ?
    """,
        (time, plant_id),
    )

    conn.commit()
    conn.close()

    schedule_all_plants()

    return jsonify({"message": "Watering time set"})


# =====================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

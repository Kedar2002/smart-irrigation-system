from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

PROFILES_DB = "profiles.db"
SENSOR_DATA_DB = "sensor_data_v1.db"
PLANT_DB = "plants.db"
PROFILES = "profiles"
SENSOR_DATA = "sensor_data_v1"
PLANTS = "plants"

# ---------------Plant Database Calls---------------

# -----------------------
# CREATE PLANT
# -----------------------
@app.route("/plant/new", methods=["POST"])
def create_plant():

    data = request.get_json()

    user_id = data.get("user_id")
    plant_name = data.get("plant_name")
    plant_type = data.get("plant_type")
    plant_age = data.get("plant_age")
    plant_height = data.get("plant_height")
    pot_type = data.get("pot_type")
    pot_size = data.get("pot_size")
    notes = data.get("notes")

    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        INSERT INTO {PLANTS}
        (user_id, plant_name, plant_type, plant_age, plant_height, pot_type, pot_size, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            user_id,
            plant_name,
            plant_type,
            plant_age,
            plant_height,
            pot_type,
            pot_size,
            notes,
        ),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Plant added successfully"}), 201

# -----------------------
# UPDATE PLANT
# -----------------------
@app.route("/plant/<int:plant_id>", methods=["PUT"])
def update_plant(plant_id):

    data = request.get_json()

    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(f"""
        UPDATE {PLANTS}
        SET plant_name = ?, plant_type = ?, plant_age = ?, plant_height = ?,
            pot_type = ?, pot_size = ?, notes = ?
        WHERE plant_id = ?
    """,
    (
        data.get("plant_name"),
        data.get("plant_type"),
        data.get("plant_age"),
        data.get("plant_height"),
        data.get("pot_type"),
        data.get("pot_size"),
        data.get("notes"),
        plant_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Plant updated"})

# -----------------------
# GET ALL PLANTS FOR USER
# -----------------------
@app.route("/plants/<int:user_id>", methods=["GET"])
def get_plants(user_id):

    conn = sqlite3.connect(PLANT_DB)
    conn.row_factory = sqlite3.Row

    plants = conn.execute(
        f"""
        SELECT * FROM {PLANTS}
        WHERE user_id = ?
        ORDER BY created_at DESC
    """,
        (user_id,),
    ).fetchall()

    conn.close()

    return jsonify([dict(p) for p in plants])

# -----------------------
# GET SINGLE PLANT
# -----------------------
@app.route("/plant/<int:plant_id>", methods=["GET"])
def get_plant(plant_id):

    conn = sqlite3.connect(PLANT_DB)
    conn.row_factory = sqlite3.Row

    plant = conn.execute(
        f"""
        SELECT * FROM {PLANTS}
        WHERE plant_id = ?
    """,
        (plant_id,),
    ).fetchone()

    conn.close()

    if plant is None:
        return jsonify({"error": "Plant not found"}), 404

    return jsonify(dict(plant))

# -----------------------
# DELETE PLANT
# -----------------------
@app.route("/plant/<int:plant_id>", methods=["DELETE"])
def delete_plant(plant_id):

    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        DELETE FROM {PLANTS}
        WHERE plant_id = ?
    """,
        (plant_id,),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Plant deleted"})

# ---------------Profiles Database Calls---------------

# -----------------------
# CREATE NEW USER PROFLIE
# -----------------------
@app.route("/profile/new", methods=["POST"])
def create_profile():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(PROFILES_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        INSERT INTO {PROFILES} (username, email, password)
        VALUES (?, ?, ?)
    """,
        (username, email, password),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Profile created successfully"}), 201

# -----------------------
# USER LOGIN
# -----------------------
@app.route("/login", methods=["POST"])
def login_profile():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(PROFILES_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    user = cursor.execute(
        f"""
        SELECT * FROM {PROFILES}
        WHERE username = ? AND password = ?
    """,
        (username, password),
    ).fetchone()

    conn.close()

    if user:
        return (
            jsonify({"message": "Login successful", "username": user["username"]}),
            200,
        )
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ---------------Sensor Data Database Calls---------------

# -----------------------
# GET PLANT DATA
# -----------------------
@app.route("/data", methods=["GET"])
def get_sensor_data():
    conn = sqlite3.connect(SENSOR_DATA_DB)
    conn.row_factory = sqlite3.Row

    data = conn.execute(
        f"""
        SELECT * FROM {SENSOR_DATA}
        ORDER BY timestamp DESC
        LIMIT 1
    """
    ).fetchone()

    conn.close()

    return jsonify(
        {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "soil": data["soil"],
            "distance": data["distance"],
            "irrigation_status": data["irrigation_status"],
            "timestamp": data["timestamp"],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import sqlite3
from datetime import datetime
from config import *

# -------------------------------
# INIT DATABASES
# -------------------------------


def init_profiles_db():
    conn = sqlite3.connect(PROFILES_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {PROFILES} (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
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
            planter_type TEXT,
            plant_age INTEGER,
            pot_size REAL,
            season TEXT,
            watering_time TEXT,
            last_irrigated DATETIME,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
            water_amount REAL,
            mode TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    conn.close()


# -------------------------------
# SAVE SENSOR DATA
# -------------------------------


def save_sensor_data(data):
    conn = sqlite3.connect(SENSOR_DATA_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        INSERT INTO {SENSOR_DATA}
        (plant_id, temperature, humidity, soil, distance, irrigation_status, water_amount, mode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data.get("plant_id"),
            data.get("temperature"),
            data.get("humidity"),
            data.get("soil"),
            data.get("distance"),
            0,
            0,
            "auto",
        ),
    )

    conn.commit()
    conn.close()


# -------------------------------
# UPDATE IRRIGATION EVENT
# -------------------------------


def log_irrigation_event(plant_id, water, mode):
    conn = sqlite3.connect(SENSOR_DATA_DB)
    cursor = conn.cursor()

    # update latest record
    cursor.execute(
        f"""
        UPDATE {SENSOR_DATA}
        SET irrigation_status = 1,
            water_amount = ?,
            mode = ?
        WHERE id = (
            SELECT id FROM {SENSOR_DATA}
            WHERE plant_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        )
    """,
        (water, mode, plant_id),
    )

    conn.commit()
    conn.close()

    # update plant last irrigated
    update_last_irrigated(plant_id)


def update_last_irrigated(plant_id):
    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        UPDATE {PLANTS}
        SET last_irrigated = CURRENT_TIMESTAMP
        WHERE plant_id = ?
    """,
        (plant_id,),
    )

    conn.commit()
    conn.close()


# -------------------------------
# GET ENRICHED DATA (ML INPUT)
# -------------------------------


def get_latest_data_with_plant(plant_id):
    conn = sqlite3.connect(SENSOR_DATA_DB)
    conn.execute(f"ATTACH DATABASE '{PLANT_DB}' AS plant_db")
    conn.row_factory = sqlite3.Row

    query = f"""
    SELECT s.*, p.plant_type, p.planter_type, p.plant_age, p.pot_size, p.season
    FROM {SENSOR_DATA} s
    JOIN plant_db.{PLANTS} p ON s.plant_id = p.plant_id
    WHERE s.plant_id = ?
    ORDER BY s.timestamp DESC
    LIMIT 1
    """

    data = conn.execute(query, (plant_id,)).fetchone()
    conn.close()

    return dict(data) if data else None


# -------------------------------
# AUTO UPDATE AGE + SEASON
# -------------------------------


def update_plant_dynamic_fields():
    conn = sqlite3.connect(PLANT_DB)
    cursor = conn.cursor()

    plants = cursor.execute(f"SELECT plant_id, created_at FROM {PLANTS}").fetchall()

    for plant_id, created_at in plants:
        created_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        age_days = (datetime.now() - created_date).days

        month = datetime.now().month
        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Summer"
        elif month in [6, 7, 8, 9]:
            season = "Monsoon"

        cursor.execute(
            f"""
            UPDATE {PLANTS}
            SET plant_age = ?, season = ?
            WHERE plant_id = ?
        """,
            (age_days, season, plant_id),
        )

    conn.commit()
    conn.close()


# -------------------------------
# HISTORY API SUPPORT
# -------------------------------


def get_irrigation_history_by_user(user_id):

    conn = sqlite3.connect(SENSOR_DATA_DB)
    conn.execute(f"ATTACH DATABASE '{PLANT_DB}' AS plant_db")
    conn.row_factory = sqlite3.Row

    query = f"""
    SELECT s.plant_id, s.timestamp, s.water_amount
    FROM {SENSOR_DATA} s
    JOIN plant_db.{PLANTS} p ON s.plant_id = p.plant_id
    WHERE p.user_id = ?
      AND s.irrigation_status = 1
    ORDER BY s.timestamp DESC
    """

    rows = conn.execute(query, (user_id,)).fetchall()
    conn.close()

    result = {}

    for row in rows:
        pid = row["plant_id"]

        entry = {"timestamp": row["timestamp"], "water": row["water_amount"]}

        if pid not in result:
            result[pid] = []

        result[pid].append(entry)

    return result


def get_plants_for_watering(current_time):
    conn = sqlite3.connect(PLANT_DB)
    conn.row_factory = sqlite3.Row

    plants = conn.execute(
        f"""
        SELECT * FROM {PLANTS}
        WHERE watering_time = ?
    """,
        (current_time,),
    ).fetchall()

    conn.close()
    return [dict(p) for p in plants]


# -------------------------------
# BASIC GETTERS (USED BY FLASK)
# -------------------------------


def get_plants_by_user(user_id):
    conn = sqlite3.connect(PLANT_DB)
    conn.row_factory = sqlite3.Row

    plants = conn.execute(
        f"SELECT * FROM {PLANTS} WHERE user_id = ?", (user_id,)
    ).fetchall()

    conn.close()
    return [dict(p) for p in plants]


def get_plant_by_id(plant_id):
    conn = sqlite3.connect(PLANT_DB)
    conn.row_factory = sqlite3.Row

    plant = conn.execute(
        f"SELECT * FROM {PLANTS} WHERE plant_id = ?", (plant_id,)
    ).fetchone()

    conn.close()
    return dict(plant) if plant else None


def get_latest_sensor_data():
    conn = sqlite3.connect(SENSOR_DATA_DB)
    conn.row_factory = sqlite3.Row

    data = conn.execute(
        f"SELECT * FROM {SENSOR_DATA} ORDER BY timestamp DESC LIMIT 1"
    ).fetchone()

    conn.close()
    return data


def get_plants_schedule():
    conn = sqlite3.connect(PLANT_DB)
    conn.row_factory = sqlite3.Row

    plants = conn.execute(
        f"""
        SELECT plant_id, user_id, watering_time
        FROM {PLANTS}
        WHERE watering_time IS NOT NULL
        """
    ).fetchall()

    conn.close()
    return [dict(p) for p in plants]

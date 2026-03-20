from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

PROFILES_DB = "profiles.db"
SENSOR_DB = "sensor_data.db"

def init_db():
    conn = sqlite3.connect(PROFILES_DB)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username REAL,
            email REAL,
            password REAL
        )
    """
    )

    conn.commit()
    conn.close()

@app.route('/profile/new', methods=['POST'])
def create_profile():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(PROFILES_DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO profiles (username, email, password)
        VALUES (?, ?, ?)
    """, (username, email, password))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Profile created successfully"
    }), 201

@app.route('/login', methods=['POST'])
def login_profile():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(PROFILES_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    user = cursor.execute("""
        SELECT * FROM profiles
        WHERE username = ? AND password = ?
    """, (username, password)).fetchone()

    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "username": user["username"]
        }), 200
    else:
        return jsonify({
            "message": "Invalid credentials"
        }), 401

@app.route('/data', methods=['GET'])
def get_sensor_data():
    conn = sqlite3.connect(SENSOR_DB)
    conn.row_factory = sqlite3.Row

    data = conn.execute('''
        SELECT * FROM sensor_data_v1
        ORDER BY timestamp DESC
        LIMIT 1
    ''').fetchone()

    conn.close()

    return jsonify({
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "soil": data["soil"],
        "distance": data["distance"],
        "irrigation_status": data["irrigation_status"],
        "timestamp": data["timestamp"]
    })

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

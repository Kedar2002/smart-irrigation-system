from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = "sensor_data_v1.db"

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_FILE)
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
    app.run(host="0.0.0.0", port=5000)

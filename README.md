# 🌱 Smart Irrigation System

An IoT-based intelligent irrigation system that automates plant watering using real-time sensor data, machine learning, and MQTT-based communication.

---

## 🚀 Overview

This project integrates **IoT devices (ESP/Arduino)** with a **Flask backend** and a **Machine Learning model** to optimize irrigation. It ensures plants receive the right amount of water based on environmental conditions and historical data.

---

## 🧠 Key Features

* 🌡️ Real-time sensor monitoring (soil moisture, temperature, humidity)
* 🤖 ML-based irrigation decision system
* 💧 Automatic & manual irrigation control
* 📊 Irrigation history tracking per plant
* 📡 MQTT-based communication between devices and backend
* 🌐 REST APIs for system interaction
* 🗂️ Multi-plant support

---

## 🏗️ System Architecture

```
[ Sensors (ESP/Arduino) ]
            ↓
      MQTT Broker (Mosquitto)
            ↓
        Flask Backend
      ↙             ↘
Database         ML Model
(SQLite)         (Prediction)
            ↓
       Irrigation Commands
```

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **IoT Communication:** MQTT (Mosquitto)
* **Hardware:** ESP8266 / Arduino
* **Machine Learning:** Scikit-learn / Pandas / NumPy
* **Scripting:** PowerShell (for system automation)

---

## 📂 Project Structure

```
backend/
│
├── flask_app.py           # Main Flask application
├── db_handler.py          # Database operations
├── mqtt_handler.py        # MQTT communication logic
├── irrigation_logic.py    # Core irrigation decision logic
├── ml_model.py            # ML model integration
├── main.py                # Entry point
├── config.py              # Configuration settings
│
├── Arduino_Multiplant_*   # Arduino code
├── ESP_Multiplant_*       # ESP8266 code
│
├── IOT_ML_Model.ipynb     # ML model training notebook
├── dataset.csv            # Training dataset
│
├── mosquitto.conf         # MQTT broker config
├── start_system.ps1       # Start script
├── stop_system.ps1        # Stop script
│
└── requirements.txt       # Python dependencies
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/Kedar2002/smart-irrigation-system.git
cd smart-irrigation-system/backend
```

---

### 🔹 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 🔹 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔹 4. Start MQTT Broker

```bash
mosquitto -c mosquitto.conf -v
```

---

### 🔹 5. Run Backend Server

```bash
python main.py
```

---

## 📡 API Endpoints (Sample)

### ▶️ Manual Irrigation

```
POST /manual_irrigation
```

### 📜 Get Irrigation History

```
GET /irrigation_history/<user_id>
```

### 🌱 Add Plant

```
POST /add_plant
```

---

## 🤖 Machine Learning

* Uses environmental + soil data
* Predicts whether irrigation is needed
* Trained on custom dataset (`.csv`)
* Integrated into backend decision logic

---

## 🔌 IoT Integration

* ESP/Arduino devices publish sensor data via MQTT
* Backend subscribes and processes data
* Commands are sent back for irrigation control

---

## ▶️ Running the Full System

1. Start MQTT broker
2. Run Flask backend
3. Power ESP/Arduino devices
4. Monitor logs for real-time data

---

## 📈 Future Improvements

* 📱 Mobile/Web dashboard
* ☁️ Cloud deployment (AWS/GCP)
* 📊 Advanced analytics & visualization
* 🌍 Weather API integration
* 🔔 Notifications (SMS/Email)

---

## 👨‍💻 Authors

**Kedar Adhikari**
M.Tech Information Technology (2025 - Pursuing)

**Vishal Ghosh**
M.Tech Information Technology (2025 - Pursuing)

---

## 📜 License

This project is open-source and available under the MIT License.

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!

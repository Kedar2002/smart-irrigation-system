import pickle
import pandas as pd

with open("watering_model_rf_v1.pkl", "rb") as f:
    model = pickle.load(f)


def parse_pot_size(pot):
    if pot is None:
        return None
    try:
        return float(str(pot).replace("L", "").strip())
    except:
        return None


def predict_water(data):

    required = [
        "temperature",
        "humidity",
        "soil",
        "plant_type",
        "plant_age",
        "pot_size",
        "season",
    ]

    if any(data.get(k) is None for k in required):
        print("❌ Missing ML fields")
        return None

    try:
        pot_size = parse_pot_size(data["pot_size"])

        if pot_size is None:
            print("❌ Invalid pot_size:", data["pot_size"])
            return None

        input_df = pd.DataFrame(
            [
                {
                    "Plant_Type": data["plant_type"],
                    "Temperature_C": data["temperature"],
                    "Humidity_%": data["humidity"],
                    "Soil_Moisture": data["soil"],
                    "Plant_Age_days": data["plant_age"],
                    "Season": data["season"],
                    "Pot_Volume_Liters": pot_size,  # ✅ FIXED
                }
            ]
        )

        water = model.predict(input_df)[0]

        return max(0, float(water))

    except Exception as e:
        print(f"ML Error: {e}")
        return None

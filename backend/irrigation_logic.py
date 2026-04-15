from ml_model import predict_water


def decide_irrigation(data):

    soil = data.get("soil")
    temp = data.get("temperature")
    humidity = data.get("humidity")

    # -------------------------------
    # SAFETY CHECK
    # -------------------------------
    if soil is None or temp is None or humidity is None:
        print("⚠️ Missing data, skipping irrigation decision")
        return 0, 0

    # -------------------------------
    # RULE 1: Extremely dry soil
    # -------------------------------
    if soil < 20:
        print("🌵 Soil very dry → Max watering")
        return 100, 1

    # -------------------------------
    # RULE 2: Moderately dry soil
    # -------------------------------
    if 20 <= soil < 40:
        water = predict_water(data)
        if water and water > 0:
            print("🌿 Moderate dryness → ML watering")
            return water, 1
        return 0, 0

    # # -------------------------------
    # # RULE 3: High humidity → avoid watering
    # # -------------------------------
    # if humidity > 80:
    #     print("🌧 High humidity → No watering")
    #     return 0, 0

    # -------------------------------
    # RULE 4: High temperature boost
    # -------------------------------
    if temp > 35:
        water = predict_water(data)
        if water:
            boosted = water * 1.2
            print("🔥 High temp → Increased watering:", boosted)
            return boosted, 1

    # -------------------------------
    # RULE 5: Soil already wet
    # -------------------------------
    # if soil > 70:
    #     print("💧 Soil wet → No watering")
    #     return 0, 0

    # -------------------------------
    # DEFAULT: ML decision
    # -------------------------------
    water = predict_water(data)
    print(water)
    if water and water > 0:
        print("🤖 ML decision → Watering:", water)
        return water, 1

    print("❌ No watering needed")
    return 0, 0

#include <ArduinoJson.h>

// Example pins
int soil1 = A0;
int soil2 = A1;

void setup() {
  Serial.begin(9600);
}

void loop() {

  // -------- PLANT 1 --------
  int soilVal1 = analogRead(soil1);

  StaticJsonDocument<200> doc1;
  doc1["plant_id"] = 101;
  doc1["temperature"] = 30;   // replace with real sensor
  doc1["humidity"] = 60;
  doc1["soil"] = soilVal1;

  serializeJson(doc1, Serial);
  Serial.println();

  delay(1000);

  // -------- PLANT 2 --------
  int soilVal2 = analogRead(soil2);

  StaticJsonDocument<200> doc2;
  doc2["plant_id"] = 102;
  doc2["temperature"] = 29;
  doc2["humidity"] = 65;
  doc2["soil"] = soilVal2;

  serializeJson(doc2, Serial);
  Serial.println();

  delay(2000);

  // -------- RECEIVE COMMAND --------
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    if (cmd.startsWith("CMD:")) {
      cmd.remove(0, 4);

      int commaIndex = cmd.indexOf(',');
      int plant_id = cmd.substring(0, commaIndex).toInt();
      int water = cmd.substring(commaIndex + 1).toInt();

      Serial.println("Command for plant: " + String(plant_id));

      if (plant_id == 101) {
        // activate pump 1
      } else if (plant_id == 102) {
        // activate pump 2
      }
    }
  }
}
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// WiFi
const char* ssid = "Kedar";
const char* password = "12345678";

// MQTT (USE IP)
const char* mqtt_server = "10.210.105.93";

WiFiClient espClient;
PubSubClient client(espClient);

// IDs
int user_id = 1;
int plant1_id = 1;
int plant2_id = 2;

// Topics
String sensorTopic1;
String sensorTopic2;
String commandTopic1;
String commandTopic2;

// ---------------- WIFI ----------------
void connectWiFi() {
  // Serial.println("Connecting to WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    // Serial.print(".");
  }

  // Serial.println("WiFi connected");
  // Serial.println(WiFi.localIP());
}

// ---------------- MQTT CALLBACK ----------------
void callback(char* topic, byte* payload, unsigned int length) {
  String message;

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  // Serial.println("MQTT Message Received");
  // Serial.println(message);

  // Parse JSON
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    // Serial.println("JSON Parse Error");
    return;
  }

  int plant_id = doc["plant_id"];
  int water = doc["water"];

  Serial.printf("CMD:%d,%d\n", plant_id, water);
}

// ---------------- MQTT RECONNECT ----------------
void reconnect() {
  while (!client.connected()) {

    // Serial.print("Connecting to MQTT...");

    if (client.connect("ESP8266Client")) {

      // Serial.println("CONNECTED");

      client.subscribe(commandTopic1.c_str());
      client.subscribe(commandTopic2.c_str());

    } else {

      // Serial.print("FAILED, rc=");
      // Serial.print(client.state());
      // Serial.println(" retrying...");

      delay(2000);
    }
  }
}

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(9600);  // MUST MATCH ARDUINO

  connectWiFi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Build topics
  sensorTopic1 = "irrigation/" + String(user_id) + "/" + String(plant1_id) + "/sensors";
  sensorTopic2 = "irrigation/" + String(user_id) + "/" + String(plant2_id) + "/sensors";

  commandTopic1 = "irrigation/" + String(user_id) + "/" + String(plant1_id) + "/command";
  commandTopic2 = "irrigation/" + String(user_id) + "/" + String(plant2_id) + "/command";
}

// ---------------- LOOP ----------------
void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  // Read from Arduino
  if (Serial.available()) {

    String data = Serial.readStringUntil('\n');

    // Serial.println("Received from Arduino:");
    // Serial.println(data);

    // Parse JSON
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, data);

    if (error) {
      // Serial.println("JSON Parse Error");
      return;
    }

    int plant_id = doc["plant_id"];

    String payload;
    serializeJson(doc, payload);

    bool success = false;

    if (plant_id == plant1_id) {
      success = client.publish(sensorTopic1.c_str(), payload.c_str());
    } 
    else if (plant_id == plant2_id) {
      success = client.publish(sensorTopic2.c_str(), payload.c_str());
    }

    // Serial.println(success ? "Published to MQTT" : "Publish failed");
  }
}
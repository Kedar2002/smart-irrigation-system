#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi
const char* ssid = "Kedar";
const char* password = "12345678";

// 🔴 IMPORTANT: USE IP, NOT HOSTNAME
const char* mqtt_server = "10.210.105.93";  // CHANGE THIS

WiFiClient espClient;
PubSubClient client(espClient);

// IDs
int user_id = 1;
int plant1_id = 101;
int plant2_id = 102;

// Topics
String sensorTopic1;
String sensorTopic2;
String commandTopic1;
String commandTopic2;

// ---------------- WIFI ----------------
void connectWiFi() {
  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.println(WiFi.localIP());
}

// ---------------- MQTT CALLBACK ----------------
void callback(char* topic, byte* payload, unsigned int length) {
  String message;

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.println("\n📩 MQTT Message Received");
  Serial.print("Topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  Serial.println(message);
}

// ---------------- MQTT RECONNECT ----------------
void reconnect() {
  while (!client.connected()) {

    Serial.print("Connecting to MQTT...");

    if (client.connect("ESP_Test_Client")) {

      Serial.println("CONNECTED");

      // Subscribe to command topics
      client.subscribe(commandTopic1.c_str());
      client.subscribe(commandTopic2.c_str());

      Serial.println("Subscribed to:");
      Serial.println(commandTopic1);
      Serial.println(commandTopic2);

    } else {

      Serial.print("FAILED, rc=");
      Serial.print(client.state());
      Serial.println(" retrying...");

      delay(2000);
    }
  }
}

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);

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
unsigned long lastPublish = 0;

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  // Publish test data every 5 seconds
  if (millis() - lastPublish > 5000) {

    lastPublish = millis();

    String payload1 = "{\"plant_id\":101,\"temperature\":30,\"humidity\":60,\"soil\":40,\"distance\":10}";
    String payload2 = "{\"plant_id\":102,\"temperature\":29,\"humidity\":65,\"soil\":45,\"distance\":12}";

    client.publish(sensorTopic1.c_str(), payload1.c_str());
    client.publish(sensorTopic2.c_str(), payload2.c_str());

    Serial.println("\n📤 Published Test Data:");
    Serial.println(sensorTopic1);
    Serial.println(payload1);
    Serial.println(sensorTopic2);
    Serial.println(payload2);
  }
}
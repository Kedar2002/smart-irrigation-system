#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "Kedar";
const char* password = "12345678";

// MQTT server
const char* mqtt_server = "10.213.128.93";

// MQTT topics
const char* sensorTopic = "irrigation/ESP001/sensors";
const char* commandTopic = "irrigation/ESP001/command";

WiFiClient espClient;
PubSubClient client(espClient);

String incomingData = "";

void callback(char* topic, byte* payload, unsigned int length) {

  String message = "";

  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.println("MQTT Command Received:");
  Serial.println(message);

  // Forward command to Arduino
  Serial.println(message); 
}

void connectWiFi() {

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void reconnectMQTT() {

  while (!client.connected()) {

    if (client.connect("ESP001")) {

      client.subscribe(commandTopic);
    }

    delay(500);
  }
}

void setup() {

  Serial.begin(9600); // Must match Arduino baud

  connectWiFi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  // Read sensor JSON from Arduino
  while (Serial.available()) {

    char c = Serial.read();

    if (c == '\n') {

      incomingData.trim();

      if (incomingData.length() > 0) {

        client.publish(sensorTopic, incomingData.c_str());
      }

      incomingData = "";
    }
    else {
      incomingData += c;
    }
  }
}
#include <dht.h>
#include <HCSR04.h>

#define dht11Pin 9 
#define relayPin 8
#define sensorPin A0
// #define LEDPIN 13

dht DHT;
HCSR04 hc(10, 11); //(trig pin , echo pin)

int readData, soilValue;
float t, h, distance;
long long targettime = 0;

long long irrigationTime = 0;

void sendJSON(){
	Serial.print("{");
  Serial.print("\"temperature\":");
  Serial.print(t);
  // Serial.print(28.4);
  Serial.print(",");

  Serial.print("\"humidity\":");
  Serial.print(h);
  // Serial.print(34.6);
  Serial.print(",");

  Serial.print("\"soil\":");
  Serial.print(soilValue);
  // Serial.print(240);
  Serial.print(",");

  Serial.print("\"distance\":");
  Serial.print(distance);
  // Serial.print(150.2);

  Serial.println("}");
}

void setup() {
  Serial.begin(9600);
  // pinMode(LED_PIN, OUTPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);
}

void loop() {

  readData = DHT.read11(dht11Pin);

  t = DHT.temperature;
  h = DHT.humidity;

  soilValue = 1023 - analogRead(sensorPin);
	
  distance = hc.dist();
	delay(60);
  String command = Serial.readStringUntil('\n');

  if (command.indexOf("water") >= 0 && irrigationTime == 0) {
    digitalWrite(relayPin, LOW);
    irrigationTime = millis();
  }

  if (millis() - irrigationTime >= 2000 && irrigationTime != 0){
    digitalWrite(relayPin, HIGH);
    irrigationTime = 0;
  }

	if (millis() - targettime > 6000){
		sendJSON();
		targettime = millis();
	}
}

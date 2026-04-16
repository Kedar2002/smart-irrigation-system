#include <ArduinoJson.h>
#include <dht.h>

// ===================== PINS =====================
#define DHT_PIN 9

#define SOIL1_PIN A0
#define SOIL2_PIN A1

#define RELAY1_PIN 7
#define RELAY2_PIN 8

#define FLOW1_PIN 2
#define FLOW2_PIN 3

#define LED_PIN 13

#define MULT 10

dht DHT;

// ===================== VARIABLES =====================

// -------- Plant 1 --------
volatile int flow1 = 0;
float vol1 = 0;
int water1 = 0;
bool irrigation_flag1 = false;
int irrigation_status1 = 0;
unsigned long lastTime1 = 0;

// -------- Plant 2 --------
volatile int flow2 = 0;
float vol2 = 0;
int water2 = 0;
bool irrigation_flag2 = false;
int irrigation_status2 = 0;
unsigned long lastTime2 = 0;

unsigned long targettime = 0;

// ===================== INTERRUPTS =====================

void flow1ISR() { 
  flow1 += MULT; 
}

void flow2ISR() { 
  flow2 += MULT; 
}

// ===================== SETUP =====================
void setup()
{
  Serial.begin(9600);

  pinMode(LED_PIN, OUTPUT);

  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);

  pinMode(FLOW1_PIN, INPUT);
  pinMode(FLOW2_PIN, INPUT);

  digitalWrite(RELAY1_PIN, HIGH);
  digitalWrite(RELAY2_PIN, HIGH);

  attachInterrupt(digitalPinToInterrupt(FLOW1_PIN), flow1ISR, RISING);
  attachInterrupt(digitalPinToInterrupt(FLOW2_PIN), flow2ISR, RISING);
}

// ===================== JSON SEND =====================
void sendJSON(int plant_id, float t, float h, int soil, int status)
{
  StaticJsonDocument<200> doc;

  doc["plant_id"] = plant_id;
  doc["temperature"] = t;
  doc["humidity"] = h;
  doc["soil"] = soil;
  doc["irrigation_status"] = status;

  serializeJson(doc, Serial);
  Serial.println();
}

// ===================== IRRIGATION =====================
void handleIrrigation()
{
  unsigned long currentTime = millis();

  // -------- PLANT 1 --------
  if (irrigation_flag1)
  {
    digitalWrite(RELAY1_PIN, LOW);  // ON

    if (currentTime - lastTime1 >= 200)
    {
      lastTime1 = currentTime;

      float flowRate = (float)flow1 / 7.5;
      float flowML = (flowRate / 600.0) * 1000.0;

      vol1 += flowML;
      flow1 = 0;
    }

    if (vol1 >= water1 && water1 > 0)
    {
      digitalWrite(RELAY1_PIN, HIGH);  // OFF

      irrigation_status1 = 1;
      irrigation_flag1 = false;

      vol1 = 0;
      water1 = 0;
    }
  }

  // -------- PLANT 2 --------
  if (irrigation_flag2)
  {
    digitalWrite(RELAY2_PIN, LOW);

    if (currentTime - lastTime2 >= 200)
    {
      lastTime2 = currentTime;

      float flowRate = (float)flow2 / 7.5;
      float flowML = (flowRate / 600.0) * 1000.0;

      vol2 += flowML;
      flow2 = 0;
    }

    if (vol2 >= water2 && water2 > 0)
    {
      digitalWrite(RELAY2_PIN, HIGH);

      irrigation_status2 = 1;
      irrigation_flag2 = false;

      vol2 = 0;
      water2 = 0;
    }
  }
}

// ===================== COMMAND =====================
void handleCommand(String cmd)
{
  cmd.trim();

  if (!cmd.startsWith("CMD:")) return;

  cmd.remove(0, 4);

  int commaIndex = cmd.indexOf(',');
  if (commaIndex == -1) return;

  int plant_id = cmd.substring(0, commaIndex).toInt();
  int water = cmd.substring(commaIndex + 1).toInt();

  if (plant_id == 1)
  {
    water1 = water;
    irrigation_flag1 = true;
    vol1 = 0;
    flow1 = 0;
  }

  if (plant_id == 2)
  {
    water2 = water;
    irrigation_flag2 = true;
    vol2 = 0;
    flow2 = 0;
  }
}

// ===================== LOOP =====================
void loop()
{
  // SERIAL READ
  static String buffer = "";

  while (Serial.available())
  {
    char c = Serial.read();

    if (c == '\n')
    {
      handleCommand(buffer);
      buffer = "";
    }
    else
    {
      buffer += c;
    }
  }

  // IRRIGATION
  handleIrrigation();

  // SENSOR SEND
  if (millis() - targettime > 5000)
  {
    DHT.read11(DHT_PIN);

    float t = DHT.temperature;
    float h = DHT.humidity;

    int soil1 = 1023 - analogRead(SOIL1_PIN);
    int soil2 = 1023 - analogRead(SOIL2_PIN);

    sendJSON(1, t, h, soil1, irrigation_status1);
    sendJSON(2, t, h, soil2, irrigation_status2);

    targettime = millis();

    irrigation_status1 = 0;
    irrigation_status2 = 0;
  }
}
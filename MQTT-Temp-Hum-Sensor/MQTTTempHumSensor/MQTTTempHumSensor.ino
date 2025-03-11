#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#include "SHT31.h"

SHT31 sht31 = SHT31();

// WiFi Credentials
const char* ssid = "MaLab";
const char* password = "MaLabG41";

const char* mqttServer = "192.168.1.104";
const int mqttPort = 1883;
const char* mqttUser = "maserver";
const char* mqttPassword = "malabpurdue";

const char* username = "lab_makeup_as";

WiFiClient espClient;
PubSubClient client(espClient);

#define RED_LED 2
#define GREEN_LED 0
#define YELLOW_LED 15

// for dht_sensor_2 ONLY since RED and GREEN switched on there:

// #define RED_LED 0
// #define GREEN_LED 2

void setup() {
  Serial.begin(9600);

  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);

  // Initialize WiFi connection
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize MQTT connection
  client.setServer(mqttServer, mqttPort);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect(username, mqttUser, mqttPassword)) {
      Serial.println("Connected to MQTT");
    } else {
      Serial.print("Failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize I2C connections
  Wire.begin();
  sht31.begin();
}

void(* resetFunc) (void) = 0; // Reset Function

void reconnectWifi() {
  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Wifi connection lost");
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Reconnecting to WiFi...");
      WiFi.begin(ssid, password);
    }
    Serial.println("Reconnected to WiFi");
  } else {
  }
}

void reconnectMqtt() {
  if (!client.connected()) {
    Serial.println("Reconnecting to MQTT...");
    if (client.connect(username, mqttUser, mqttPassword)) {
      Serial.println("Reconnected to MQTT");
    } else {
      Serial.print("Failed with state ");
      Serial.println(client.state());
      resetFunc(); // Reset Pi 
    }
  }
}

void loop() {
  StaticJsonDocument<200> doc;
  char output[200];

  float temp = sht31.getTemperature();
  float hum = sht31.getHumidity();

  if (!client.connected()) {
    Serial.println("MQTT Error");
    digitalWrite(RED_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
  } else {
    digitalWrite(RED_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
  }

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT Error");
    digitalWrite(YELLOW_LED, HIGH);
  } else {
    digitalWrite(YELLOW_LED, LOW);
  }

  doc[String(username)+"_temp"] = temp;
  doc[String(username)+"_hum"] = hum;

  serializeJson(doc, output);
  Serial.println(client.connected());
  client.publish("lab_weather/", output);

  reconnectWifi();
  reconnectMqtt();

  client.loop();

  delay(5000);
}


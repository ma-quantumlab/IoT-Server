# Adding Data Source

This guide walks you through the process of fetching data from an MQTT broker in Node-RED and sending it to an InfluxDB instance for storage and analysis.

## Introduction

This tutorial will walk through step by step on how to take data from any device and pass it through the Raspberry Pi and have it visible on Grafana. To start the user must be familiar with the overall flow of the server shown below, this is explained in the README.md file. To begin this is 

<img src="https://github.com/user-attachments/assets/e60e50c4-e6c8-4d2b-a466-b174586ae207" alt="Model" width="600">

Additionally the user should also understand the basic structure of Influx DB. Influx DB stores data in different databases, for these databases certain retention policies can be set to mark how much data should be stored locally, it is set for 2 weeks. In each database there are different measurments that correspond to different collections of data being stored, and finally for each measurment there are a certain number of feilds within each. For example in the database "Fridges" the measurment "Alice Temperature" is shown below (this data is taked from the /ServerData folder in Dropbox where for each day there is a list of CSV files which represent all of the measruments in all the databases). Notice for the measurment "Alice Temperature" there are four corresonding fields. 

| Time                   | Alice Temperature 4K | Alice Temperature 50K | Alice Temperature MXC | Alice Temperature Still |
|:-----------------------|:--------------------:|:---------------------:|:---------------------:|-------------------------:|
| 2024-12-01 19:35:14.440916 | 3.11189            | 47.3277              | 0.0096873            | 0.803631                |
| 2024-12-01 19:35:17.461198 | 3.11189            | 47.3277              | 0.0096873            | 0.803631                |
| 2024-12-01 19:35:20.486014 | 3.11189            | 47.3277              | 0.0096873            | 0.803631                |


## Step 1: Send Data through MQTT to Raspberry Pi 

In order to add a data source to be viewed on Grafana the user must first send the data to the Pi via the MQTT protocol. This can be done on almost any device such as a computer or arduino and implemented through a simple python or arduino script.

Although both python and arduino will differ in the code that accomplishes this task the idea is about the same. The process is the same, we first configure MQTT to connect the device to the Raspberry Pi, then we get the data and load it into a JSON file containing the different fields within the measurement and finally we send the data.  

### Python Script Example:

``` python
import json
import time
import random
import paho.mqtt.client as mqtt

# MQTT Configuration
mqtt_broker_host = "mqtt_broker_host"  # Replace with our MQTT broker's host
mqtt_broker_port = 1883  
mqtt_topic = "topic"  # Replace with our MQTT topic
mqtt_username = "your_username"  # Replace with our MQTT username
mqtt_password = "your_password"  # Replace with our MQTT password

# Set up MQTT client and connect
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(mqtt_username, mqtt_password)

if __name__ == "__main__":

    while True:

        client.connect(mqtt_broker_host, mqtt_broker_port)

        # Generate data
        data = {
            "temperature": round(random.uniform(0, 100), 3),  # Generate Random Number
            "humidity": round(random.uniform(0, 100), 3),     # Generate Random Number
        }

        # Convert data to JSON and publish
        mqtt_payload = json.dumps(data)
        client.publish(mqtt_topic, mqtt_payload)
        print(f"Sent MQTT message: {mqtt_payload}")

        # Wait for 5 seconds before sending the next data
        time.sleep(5)

```

### Arduino Script Example:

``` c++
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// MQTT Configuration and WIFI Cridentials
const char* ssid = "MaLab";
const char* password = "******"; // MaLab Password

const char* mqttServer = "192.168.1.104";
const int mqttPort = 1883;
const char* mqttUser = "maserver"; // Replace with our MQTT username
const char* mqttPassword = "malabpurdue"; // Replace with our MQTT password

const char* username = "mix_alice"; // Same as topic name 

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600);

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
}

void loop() {
  StaticJsonDocument<200> doc;
  char output[200];

  float temp = float randomFloat = random(0, 10000) / 100.0; // Generate Random Number
  float hum = float randomFloat = random(0, 10000) / 100.0; // Generate Random Number


  // Convert data to JSON and publish
  doc[String(username)+"_temp"] = temp;
  doc[String(username)+"_hum"] = hum;

  serializeJson(doc, output);
  Serial.println(client.connected());
  client.publish("lab_weather/", output);

  client.loop();

  // Wait for 5 seconds before sending the next data
  delay(5000);
}
```

To view programs created in Python that send data via MQTT navigate to the /Bluefors-Log-Watcher folder and to see programs created in Arduino navigate to the /MQTT-Chilled-Water-Monitor and /MQTT-Temp-Hum-Sensor folders within this repository. 

To assure the data is being sent to the Raspberry Pi you can log onto the server (via typing `ssh malab@192.168.1.104` into any computer in the ) and type in the command `listen`. This command is a bash alias for the command `mosquitto_sub -h localhost -t "#" -v` which returns what are the raw JSON values that are being received by the server. Note however this will list all of the incoming JSON values so it is smart to filter with a command like grep to see if the topic that was configured is coming through. This is done below for the topic "fridges":

``` bash
malab@maserver:~ $ listen | grep "fridges_"
lab_weather/ {"fridges_temp":22.19081497,"fridges_hum":16.40192223}
lab_weather/ {"fridges_temp":22.1614399,"fridges_hum":16.38361168}
lab_weather/ {"fridges_temp":22.1614399,"fridges_hum":16.39887047}
```

Note to the left it shows the MQTT channel that it is being published on. 

## Step 2: 

Once the data is received by the Raspberry Pi it will need to be passed into Influx DB, and this is done through Node-RED. To access Node-RED the following url can be used on any device that is connected to the MaLab internet: "http://192.168.1.104:1880". Once on the Node-RED the following flow will be noticed, depending on how long it has been the flow may be changed partially however the overall structure should remain the same:

<img src="https://github.com/user-attachments/assets/c2e99a0e-99a3-488b-843e-19dd6c186d5a" alt="Model" width="600">

The data is first queried with the MQTT In blocks then it is passed into the Assign Labels block which takes the MQTT topics and assigns them feild names and then finally depending on which Measurment 


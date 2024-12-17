# Adding Data Source

This guide walks you through the process of fetching data from an MQTT broker in Node-RED and sending it to an InfluxDB instance for storage and analysis.

## Introduction

This tutorial provides a step-by-step guide on how to collect data from various devices, process it through a Raspberry Pi, and visualize it using Grafana. Before diving in, it's important to understand the overall flow of the server architecture, as illustrated in the diagram below and explained in the `README.md` file. To get started, ensure the data is being sent from the measurement devices to the Raspberry Pi.

<p align="center">
  <img src="https://github.com/user-attachments/assets/e60e50c4-e6c8-4d2b-a466-b174586ae207" alt="Model" width="600">
</p>

Additionally, users should have a basic understanding of the structure of InfluxDB. In short InfluxDB organizes data into databases, where retention policies determine how long the data is stored locally. By default, this is set to five weeks. Within each database, data is categorized into measurements, which represent collections of related data points, and each measurement contains multiple fields that store individual data streams. For example, in the database "Fridges", the measurement "Alice Temperature" is shown below. In the "Alice Temperature" measurement, there are four corresponding fields, each representing a distinct stream of data. Visit the `DatabaseFlow.md` file to view all of the Databases that are currently active and their different measurements.

| Time                   | Alice Temperature 4K | Alice Temperature 50K | Alice Temperature MXC | Alice Temperature Still |
|:-----------------------|:--------------------:|:---------------------:|:---------------------:|-------------------------:|
| 2024-12-01 19:35:14.440916 | 3.11189            | 47.3277              | 0.0096873            | 0.803631                |
| 2024-12-01 19:35:17.461198 | 3.11189            | 47.3277              | 0.0096873            | 0.803631                |
| 2024-12-01 19:35:20.486014 | 3.11189            | 47.3277              | 0.0096873            | 0.803631                |


## Step 1: Send Data through MQTT to Raspberry Pi 

To add a data source for visualization in Grafana, the data must first be sent to the Raspberry Pi using the MQTT protocol. This can be achieved from almost any device, such as a computer or an Arduino, using a simple Python or Arduino script.

While the code for Python and Arduino may differ, the underlying process remains the same. First, MQTT is configured to establish a connection between the device and the Raspberry Pi. Next, the data is gathered and structured into a JSON file, with each field representing a specific data point within the measurement. Finally, the data is sent to the Raspberry Pi.

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
const char* password = "********"; // MaLab Password

const char* mqttServer = "192.168.1.104";
const int mqttPort = 1883;
const char* mqttUser = "maserver"; // Replace with our MQTT username
const char* mqttPassword = "malabpurdue"; // Replace with our MQTT password

const char* username = "topic"; // Same as topic name 

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

To view actively running programs written in Python that send data via MQTT, navigate to the `/Bluefors-Log-Watcher` folder. For programs created in Arduino, refer to the `/MQTT-Chilled-Water-Monitor` and `/MQTT-Temp-Hum-Sensor` folders within this repository.

To ensure that data is being sent to the Raspberry Pi, log onto the server by typing ssh malab@192.168.1.104 from any computer. Once connected, use the command listen. This is a bash alias for `mosquitto_sub -h localhost -t "#" -v`, which outputs all incoming raw JSON values received by the server.

Since this command displays all incoming topics, it’s helpful to filter the output using a tool like `grep` to isolate the specific topic you’re monitoring. For example, to check for data under the topic "fridges", you can use the following command:

``` bash
malab@maserver:~ $ listen | grep "fridges_"
lab_weather/ {"fridges_temp":22.19081497,"fridges_hum":16.40192223}
lab_weather/ {"fridges_temp":22.1614399,"fridges_hum":16.38361168}
lab_weather/ {"fridges_temp":22.1614399,"fridges_hum":16.39887047}
```

Note to the left it shows the MQTT channel that it is being published on. 

## Step 2: 

Once the data is received by the Raspberry Pi, it needs to be sent to InfluxDB, which is accomplished using Node-RED. To access Node-RED, navigate to port 1882 on the Raspberry Pi (e.g., `http://<raspberry-pi-ip>:1880`). On the Node-RED interface, you will see a predefined flow. While minor changes may occur over time, the overall structure of the flow should remain consistent.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c2e99a0e-99a3-488b-843e-19dd6c186d5a" alt="Model" width="800">
</p>

The data is first received using MQTT In blocks. It is then passed into the Assign Labels block, which maps the MQTT topics to their respective field names. Finally, the fields are split into separate InfluxDB Out blocks, with each block representing a specific measurement.

To add an additional data source, the user must connect it to the flow. This can be done by duplicating an existing MQTT In node and editing its topic to match the name of the new data being published. The MQTT In node, as shown in the image on the left, allows the user to specify the topic where the new data is being sent.

<p align="center">
  <img src="https://github.com/user-attachments/assets/31063c94-6724-464e-b9f6-9c4b462ec5d1" alt="Model" width="800">
</p>

Once the MQTT In node is configured, it must be connected to the Assign Labels block. In this block, the user needs to add a new section to the devices list within the JavaScript code to map the appropriate measurement names to their corresponding values. An example snippet is provided below, and the full implementation can be found in the `NodeREDAssignMeasurements.js` file located in the Subprocesses directory. Be sure to update this file whenever changes are made before deploying.

After updating the code, the user must ensure that the number of outputs in the Assign Labels block matches the largest index specified in the array. For instance, if the largest index in the devices list is 16, the block must have 17 outputs. The number of outputs can be adjusted in the setup tab of the Node-RED block. 

```
let devices = [
...
{ 
  index: 16, 
  fields: ['new_field', ...], 
  labels: ['New Field', ...]
}
...
]
```

Finally, the user must connect the new output of the Assign Labels block to an InfluxDB Out node, which stores the data in InfluxDB. To do this, the user can duplicate an existing InfluxDB Out node. When configuring the node, the user must specify the correct measurement name for logging the data and select the appropriate database to store it in. An example of a properly configured block is shown in the image below.

Once these steps are completed, the new data source will be successfully added and can now be visualized in Grafana.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4783fcbc-d8ea-464a-8b32-02f258d616f0" alt="Model" width="600">
</p>

## Step 3: 

Now that the data has been successfully passed into InfluxDB, it can be displayed on the Grafana front end. From this point, the system will automatically upload the data to Dropbox daily.

To add a visualization to any of the Grafana dashboards, navigate to the desired dashboard and click the blue "Add" button at the top. From the dropdown menu, select "Visualization". The image below provides an example of how to configure a Grafana visualization, with the following key steps to note:

Select the correct InfluxDB data source: Each database is paired with a specific data source.

Configure the query:

- Under MEASUREMENT, choose the measurement of interest.
- Below that, select the desired FIELD.
  - For example in the image, the field "Alice 50K Temperature" was selected from the measurement "alice_temperature" within the fridges database.
- The "fill(previous)" option in the GROUP BY section is optional but helps ensure the graph appears continuous.
- Choose the visualization type: Grafana offers a variety of visualization options located at the top-right. In this example, the "Stat" visualization was selected.
- Finalize the visualization: Give the visualization a name and, optionally, add a description for clarity.

Once these steps are completed, the visualization is ready and can be viewed within the Grafana dashboard.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9a53c61b-fc08-4d04-95a5-8489195b6cf3" alt="Model" width="1000">
</p>

## Step 4: 

Finally, the user must add the new data source to the Alert API Configuration file so that alerts can be paired with it. The `alerts_config.json` file is located in the `/Python-APIs/Alert-Config-Files/` folder, and the new section must be added to the alerts array within the file.

To edit this file, secure shell (SSH) into the server and run the following command:

``` bash
malab@maserver:~ $ alerts --edit "Alerts Config"
```

This will open the file in an editor for modification. The example below demonstrates how the "Alice 50K Temperature" section is added to the configuration file. Any new field must follow the same format. Be sure to include the database name, measurement name, and field name in the configuration file, ensuring they match exactly with the names set up previously. 

If there is any confusion regarding the database structure or naming, refer to the `DatabaseFlow.md` document, which contains all current names. When adding new names, update this document so new users can remain informed. Once the changes are completed, the API will prompt the user to push the updates to Git. It is highly recommended to push these changes so all users have access to the latest alert configuration file.

``` json
{
    "name":"Alerts Config",
    "alerts":
    [
      ...
        {
            "title":"Alice 50 K Temperature",
            "database":"fridge_database",
            "measurement":"alice_temperature",
            "field":"Alice Temperature 50K",
            "nodata":"OK",
            "dashboardname":"Alice Fridge Dashboard"
        },
      ...
    ]
}
```

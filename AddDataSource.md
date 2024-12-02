# Guide: Connecting MQTT to InfluxDB in Node-RED

This guide walks you through the process of fetching data from an MQTT broker in Node-RED and sending it to an InfluxDB instance for storage and analysis.

---

## Prerequisites

1. **Node-RED** installed and running.
2. An **MQTT broker** (e.g., Mosquitto) set up and running.
3. An **InfluxDB** instance installed and configured.
4. Necessary Node-RED nodes installed:
   - `node-red-contrib-mqtt-broker`
   - `node-red-contrib-influxdb`

---

## Step 1: Fetch Data from MQTT in Node-RED

1. Open your Node-RED dashboard.
2. Drag an `MQTT in` node onto the workspace.
3. Double-click the `MQTT in` node to configure it:
   - **Server**: Add your MQTT broker’s URL (e.g., `mqtt://localhost:1883`).
   - **Topic**: Enter the topic you want to subscribe to (e.g., `sensor/temperature`).
4. Optionally, configure Quality of Service (QoS) and output format.
5. Click **Done**.

---

## Step 2: Transform Data (Optional)

1. Drag a `function` or `change` node if you need to process or format the MQTT payload before sending it to InfluxDB.
2. For example, if your MQTT payload is JSON, you can use a `function` node to extract specific fields:
   ```javascript
   const payload = JSON.parse(msg.payload);
   msg.payload = {
       measurement: "temperature",
       fields: {
           value: payload.value,
       },
       tags: {
           location: payload.location,
       }
   };
   return msg;

# IoT-Server
IoT Server for Quantum Information Lab

## Introduction 

This IoT Server was created on a Raspberry Pi V4 in order to have a centralized system of storing different parameters from measurement devices from within the lab. This was done through the four different programs:

- Mosquito
- NodeRED 
- Influx DB
- Grafana 

## Basic Flow

The basic flow of this server follows the diagram below: 

<img src="https://github.com/user-attachments/assets/e60e50c4-e6c8-4d2b-a466-b174586ae207" alt="Model" width="600">

---

## Background and Features

### Flow of Data
1. Measurement data is published on different MQTT channels from various IoT devices in the network.
2. Node-RED subscribes to the different MQTT topics and retrieves JSON data from the devices.
3. After parsing the JSON values, Node-RED pushes the data to Influx DB to be stored as a time-series value.
4. Grafana queries data from Influx DB to display it on the front-end interface hosted on the Raspberry Pi.

### Server Features
- All services run locally on Docker containers to improve efficiency.
- Alerts in Grafana notify lab personnel via email and Slack when thresholds are exceeded.
- A Python API enables command-line interaction with the server interface.
- SSH (Secure Shell Protocol) allows remote access to data and APIs across the network.

### Python API Highlights
- Users can enable, disable, create, edit, and delete alerts using JSON text files for bulk editing.
- Alerts and contact points are configured in Grafana through Prometheus, and changes are viewable on the Grafana dashboard.
- Influx DB is configured with a retention policy of two weeks, and a script formats data into CSV files for remote storage via Dropbox.

---

## Key Technologies and Tools

- **MQTT (Message Queuing Telemetry Transport)**: A lightweight protocol for efficient, low-latency communication between devices.
- **Node-RED**: A low-code development tool for visual programming, used to manage device data flow.
- **Influx DB**: A time-series database for storing and querying measurement data.
- **Grafana**: An interactive visualization tool for monitoring and alerting.
- **Docker**: Containerization platform ensuring lightweight, isolated deployments.
- **Dropbox**: Used for remote storage of CSV-formatted data via API integration.
- **SSH**: Provides secure remote access to the server and APIs.

---

## Current and Future Work

1. **Front-End GUI**: Developing a graphical interface to complement the command-line API.
2. **JSON Integration**: Transitioning fully to JSON files for easier configuration and data handling.
3. **Version Control**: Expanding version control to facilitate adoption by other labs.
4. **Enhanced Protocol Integration**: Ensuring data consistency across IoT devices by standardizing protocols.

---

## References

This work was supported by the collaborative efforts of the Purdue Ma Lab. Special thanks to:
- Dr. Alex Ruichao Ma for his guidance.
- The Ma Lab team for their support and feedback.

For further information about server contact Dhruv Upreti

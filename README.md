# IoT-Server
IoT Server for Quantum Information Lab

## Alerts API:

The alerts API is a command line tool designed to allow users to view, edit, create or delele alerts that are associated with Grafana and Influx DB directly from the command line. In order to use the alerts API the user must have atleast the `alerts_config.json` file which defines all of the different alerts and their configurations. To invoke the api type the following in

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
-----------     Alerts     -----------
```a

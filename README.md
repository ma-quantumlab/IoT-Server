# IoT-Server
IoT Server for Quantum Information Lab
## Basic Flow

This IoT server was created in order to 

## Alerts API



The alerts API is a command line tool designed to allow users to view, edit, create or delele alerts that are associated with Grafana and Influx DB directly from the command line. Alerts additionally have configuration files that store large lists of alerts so the user can simply edit the configuration JSON instead of editing individual alerts. 

In order to use the alerts API the user must ssh onto the MaLab server. The simplest action one can perform with this tool is to simply view the status of the alerts and view which configration files are avalible. To do this 

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
-----------     Alerts     -----------
```



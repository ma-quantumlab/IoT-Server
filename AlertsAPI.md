# Alerts API

The alerts API is a command line tool designed to allow users to view, edit, create and delele alerts that are associated with Grafana and Influx DB. Alerts additionally have configuration files that store large lists of preconfigured alerts so the user can simply edit the configuration JSON instead of editing individual alerts. 

In order to use the alerts API the user must ssh onto the MaLab server. The simplest action one can perform with this tool is to simply view the status of the alerts and view which configration files are avalible. To do this simply invoke `alerts` in the command line as shown below.

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
```

From the output we see that under the "Configurations" section there are the 3 configuration files shown; any file in the /IoT-Server/Alerts-API that ends with `config.json` will be automatically considered a configuration file. Additinoally there are no Alerts defined yet. 

Additionally there is another file, the `alerts_config.json` file which defines how each alert is set up; unless a user is adding an additional datasource this file should not be edited. 

## Setting Alert Configuration 

Most of what users will do is set different alert configurations. As described above all alert configurations can be viewed when invoking the `alerts` command. A typical alert configuration file is structured as shown below, in this example we are looking at the "Test" configuration file:

``` json
{
    "name":"Test",
    "description":"for alert api demo",
    "alerts":
    [
        {
            "title":"Alice 50 K Temperature Upper Warning Alert",
            "threshold":50,
            "state":"ON"
        },
        {
            "title":"Alice 4 K Temperature Upper Warning Alert",
            "threshold":4,
            "state":"ON"
        }
    ]
}
```

The user can edit the threshold (any float value) or state ("ON" or "OFF") section, the names of the alerts follow a specifc pattern that allows for no repeats and for the program to recognize properties of the alert. These should generally not be edited, refer to the Alerts Name Nomenclature section if so. In order to enable the configuration file type `alerts --config "<configuration name>"`. Below is an example with the "Test" configuration file. If no error occurs you should see an output with the new alerts configured. 

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --config "Test"
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
Name: 'Alice 4 K Temperature Upper Warning Alert'        | Threshold: Greater than 4            | State: ON
```

## Deleting Alerts

To delete an alert type `alerts --delete "<alert name>"` into the command line. It is possible to delete multiple alerts at once; for example if one is intrested in deleting all alerts that contain the word "Warning" the following command can be invoked `alerts --delete "Warning"`. If the user is intrested in deleting every alert the following command can be invoked `alerts --delete "*"`. Below is an example of what deleting an alert would appear as.

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
Name: 'Alice 4 K Temperature Upper Warning Alert'        | Threshold: Greater than 4            | State: ON
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --delete "Alice 4 K Temperature Upper Warning Alert"
Are you sure you want to delete: 'Alice 4 K Temperature Upper Warning Alert'? It is irreversible! (Y/n) Y
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
```

## Edit Alert Value

To edit a single alert value type `alerts --name "<alert name>" --threshold <new threshold value>` where the threshold value can be any floating point number. One can only edit one alert at a time. Below is an exmaple of what editing an alert would appear as.

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --name "Alice 50 K Temperature Upper Warning Alert" --threshold 999.111
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 999.111      | State: ON
```

## Edit Alert State

To edit a the state of alerts type `alerts --name "<alert name>" --state "<new state value>"` where new state can only take values "ON" or "OFF". It is possible to edit the state of multiple alerts at once by passing in a string that is contained in the alerts you want to change. For example to set the state of all alerts containing the word "Warning" to "OFF" one would type the command `alerts --name "Warning" --state "OFF"`. Below shows an example of this. 

```
malab@maserver:~/IoT-Server $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
Name: 'Alice 4 K Temperature Upper Warning Alert'        | Threshold: Greater than 4            | State: ON
malab@maserver:~/IoT-Server $
malab@maserver:~/IoT-Server $
malab@maserver:~/IoT-Server $
malab@maserver:~/IoT-Server $ alerts --name "Warning" --state "OFF"
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: OFF
Name: 'Alice 4 K Temperature Upper Warning Alert'        | Threshold: Greater than 4            | State: OFF
```

## Creating Alerts

Creating alerts are more invoed than simply editing or deleting them. The user can create new alerts by editing the configuraiton JSON to include additinoal alerts, however they are only bounded by the alerts that are defined within the `alerts_config.json` file. In order to create new alerts with Influx DB query sources that are not defined within the `alerts_config.json` file the user must have an adequite understanding of how Grafana queries and displays data from Influx DB, more information can be found in the README.md file.

It is assumed the reader understands the high level overview of how Grafana queries data from Influx DB. There are two possible alerts the user can create, an alert that triggers when a value surpasses a threshold (typically called an "Upper" alert), or an alert that triggers when a value goes under a threshold (typically called a "Lower" alert). For each type of alert there is a further subset, a "Warning" alert and a "Critical" alert. 

In total there are four types of alerts that can be created. In order to create an alert the user must define the threshold and the initial state it should be placed in which can both be changed as demonstrated above. To create the alert type `alerts <alert type flag> --threshold <threshold value> --state <state value>` where the alert type flag can be one of the four values mentioned above: `--create_upper_critical`, `--create_lower_critical`, `--create_upper_warning`, `--create_lower_warning`.

An example of a possible alert request with threshold value 999 and initial state "ON" is shown below. 
```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --create_upper_critical --threshold 999 --state "ON"
Creating alert ... Enter in values below:
Choose Influx DB databases, or number from list:
0. fridge_database
1. water_chiller_database
2. weather_database
Name or Index: 0
```
Immediatly after the request is sent the program will first request which Influx Database the user wishes to query data from; in this example the "fridge_database" was chosen. Following that the program will request you chose a measurment from the respective list of possible measurments within that database to query from in this example the user chose "alice_temperature" 
```
Choose Measurement from database fridge_database, or number from list:
0. alice_compressor
1. alice_flowmeter
2. alice_pressure
3. alice_temperature
4. bob_compressor
5. bob_flowmeter
6. bob_pressure
7. bob_temperature
Name or Index: 3
```
Finally the program will request the user to chose a feild from the measurment chose above; in this example the feild "Alice Temperature 50K" was chosen. 
```
Choose field from measurement alice_temperature, or number from list:
0. Alice Temperature 4K
1. Alice Temperature 50K
2. Alice Temperature MXC
3. Alice Temperature Still
Name or Index: 1
```
Following this the program will prompt the user to 
```
Enter name: Alice 50 K Temperature
State alert when NO DATA? ('OK'/'Alerting') OK
Configure dashboard-alert pair? ('y'/'n') y
```
```
Choose dashboard names, or number from list:
0. Alice Fridge Dashboard
1. Bob Fridge Dashboard
2. Lab Weather Dashboard
3. Main Lab Dashboard
4. Water Chiller Dashboard
Name or Index: 0
```
```
Choose timeseries panel names, or number from list:
0. Alice 50 K Temperature
1. Alice 4 K Temperature
2. Alice Still Temperature
3. Alice MXC Temperature
4. Alice Flowmeter
5. Alice OVC Pressure
6. Alice Still Pressure
7. Alice Differential Pressure
8. Alice Tank Pressure
9. Alice Compressor Water In
10. Alice Compressor Water Out
11. Alice Compressor Oil Temperature
12. Alice Compressor Error Status
Name or Index: 0
```
```
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: for alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: for pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Critical Alert'      | Threshold: Greater than 999          | State: ON
```



## Alert Naming Nomenclature

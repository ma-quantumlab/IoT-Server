# Alerts API

## Getting Started 

The alerts API is a command line tool designed to allow users to view, edit, create and delete alerts that are associated with Grafana and Influx DB. Alerts additionally have configuration files that store large lists of pre-configured alerts so the user can simply edit a configuration JSON instead of editing individual alerts through the API. 

To view the grafana dashboards go to [this link](http://192.168.1.104:3000/dashboards) on any computer connected to the server (The username is on the lab OneNote page). 

In order to use the alerts API the user must ssh onto the MaLab server. To do this one simply has to enter a command line (on a computer connected to the internet) and type `ssh malab@192.168.1.104` and then type in the password "malabserver" into the prompt. Once the user is in the server they will have access to the alerts API. 

The simplest action one can perform with this tool is to simply view the status of the alerts and view which configuration files are available. To do this simply invoke `alerts` in the command line as shown below.

``` bash
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
```

From the output we see that under the "Configurations" section there are the 4 configuration files shown. As shown under the "Alerts" section, there are no Alerts defined yet. 

Alerts will be visible directly on any time-series panel that queries the same Influx DB data as the alert; when we set up the four alerts below, the Grafana panel will make this visible. 

``` bash
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Lower Critical Alert'      | Threshold: Less than 47.05           | State: ON
Name: 'Alice 50 K Temperature Lower Warning Alert'       | Threshold: Less than 47.07           | State: ON
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 47.09        | State: ON
Name: 'Alice 50 K Temperature Upper Critical Alert'      | Threshold: Greater than 47.1         | State: ON
```

The Grafana time-series panel shades in "red"/"dark-red" or "orange"/"dark-orange" regions for the different types of alerts.

<img width="1303" alt="Screenshot 2024-11-10 at 11 36 56 AM" src="https://github.com/user-attachments/assets/cfa209b3-00db-4f73-9217-afef459f05af">

There are many different things one can do with the API. 

- Visit [Enabling Alert Configurations](#enabling-alert-configurations) if the user is interested in setting up an alerts configuration file
- Visit [Deleting Alerts](#deleting-alerts) to learn how to delete certain alerts
- Visit [Edit Alert Value](#edit-alert-value) to edit certain alert values
- Visit [Edit Alert State](#edit-alert-state) to edit certain alert states
- Visit [Creating Alerts](#creating-alerts) to create new alerts via the API (for the most part users will create alerts via configuration files)
- [(Optional) Alert Naming System](#alert-naming-system)

## Enabling Alert Configurations

Most of what users will do is set different alert configurations. As described above all alert configurations can be viewed when invoking the `alerts` command. A typical alert configuration file is structured as shown below, in this example we are looking at the "Test" configuration file:

``` json
{
    "name":"Test",
    "short-description":"alert api demo",
    "long-description":"...",
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

The user can edit the threshold (any float value) or state ("ON" or "OFF") section, the names of the alerts follow a specific pattern that allows for no repeats and for the program to recognize properties of the alert. These should generally not be edited, refer to the [Alert Naming System Section](#alert-naming-system) section if so. In order to enable the configuration file type `alerts --config "<configuration name>"`. Below is an example with the "Test" configuration file. If no error occurs you should see an output with the new alerts configured. 

``` bash
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --config "Test"
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
Name: 'Alice 4 K Temperature Upper Warning Alert'        | Threshold: Greater than 4            | State: ON
```

If the user is interested in creating a new configuration file they must first assure that the measurements that want to be used are defined within the `alert_config.json` file. To create the configuration file that configures the same alerts shown in the panel image above the `alert_config.json` must contain a "Alice 50 K Temperature" section as shown below:

``` json
{
    "name":"Alerts Config",
    "alerts":
    [
        {
            "title":"Alice 50 K Temperature",
            "database":"fridge_database",
            "measurement":"alice_temperature",
            "field":"Alice Temperature 50K",
            "nodata":"OK",
            "dashboardname":"Alice Fridge Dashboard"
        }
    ]
}
```

Below is what a configuration file would look like which creates four different alerts; realize that the configuration file must end in "config.json" and be in the `~/Python-APIs/Alert-Config-Files/` folder to be recognized by the program. Notice how the type of alert is defined within the title section, the title must follow the specifications outlined in the [Alert Naming System Section](#alert-naming-system).

``` json
{
    "name":"Test Config File",
    "short-description":"alert api demo",
    "long-description":"...",
    "alerts":
    [
        {
            "title":"Alice 50 K Temperature Lower Critical Alert",
            "threshold":47.05,
            "state":"ON"
        },
        {
            "title":"Alice 50 K Temperature Lower Warning Alert",
            "threshold":47.07,
            "state":"ON"
        },
        {
            "title":"Alice 50 K Temperature Upper Warning Alert",
            "threshold":47.09,
            "state":"ON"
        },
        {
            "title":"Alice 50 K Temperature Upper Critical Alert",
            "threshold":47.1,
            "state":"ON"
        }
    ],
    "longdescription":"..."
}
```

## Deleting Alerts

To delete an alert type `alerts --delete "<alert name>"` into the command line. It is possible to delete multiple alerts at once; for example if one is interested in deleting all alerts that contain the word "Warning" the following command can be invoked `alerts --delete "Warning"`. If the user is interested in deleting every alert the following command can be invoked `alerts --delete "*"`. Below is an example of what deleting an alert would appear as.

``` bash
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
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
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
```

## Edit Alert Value

To edit a single alert value type `alerts --name "<alert name>" --threshold <new threshold value>` where the threshold value can be any floating point number. One can only edit one alert at a time. Below is an example of what editing an alert would appear as.

``` bash
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --name "Alice 50 K Temperature Upper Warning Alert" --threshold 999.111
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 999.111      | State: ON
```

## Edit Alert State

To edit a the state of alerts type `alerts --name "<alert name>" --state "<new state value>"` where new state can only take values "ON" or "OFF". It is possible to edit the state of multiple alerts at once by passing in a string that is contained in the alerts you want to change. For example to set the state of all alerts containing the word "Warning" to "OFF" one would type the command `alerts --name "Warning" --state "OFF"`. Below shows an example of this. 

``` bash
malab@maserver:~/IoT-Server $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
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
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: OFF
Name: 'Alice 4 K Temperature Upper Warning Alert'        | Threshold: Greater than 4            | State: OFF
```

## Creating Alerts

Creating alerts are more involved than simply editing or deleting them. The user can create new alerts by editing the configuration JSON to include additional alerts, however they are only bounded by the alerts that are defined within the `alerts_config.json` file. 

It is assumed the reader understands the high level overview of how Grafana queries data from Influx DB. There are two possible alerts the user can create, an alert that triggers when a value surpasses a threshold (typically called an "Upper" alert), or an alert that triggers when a value goes under a threshold (typically called a "Lower" alert). For each type of alert there is a further subset, a "Warning" alert and a "Critical" alert. 

In total there are four types of alerts that can be created. In order to create an alert the user must define the threshold and the initial state it should be placed in which can both be changed as demonstrated above. To create the alert type `alerts <alert type flag> --threshold <threshold value> --state <state value>` where the alert type flag can be one of the four values mentioned above: `--create_upper_critical`, `--create_lower_critical`, `--create_upper_warning`, `--create_lower_warning`.

An example of a possible alert request with threshold value 999 and initial state "ON" is `alerts --create_upper_critical --threshold 999 --state "ON"`. After the initial  

```
Creating alert ... Enter in values below:
Choose Influx DB databases, or number from list:
0. fridge_database
1. water_chiller_database
2. weather_database
Name or Index: 0
```

Immediately after the request is sent the program will first request which Influx Database the user wishes to query data from; in this example the "fridge_database" was chosen. Following that the program will request you chose a measurement from the respective list of possible measurements within that database to query from in this example the user chose "alice_temperature" 

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

Finally the program will request the user to chose a field from the measurement chose above; in this example the field "Alice Temperature 50K" was chosen. 

```
Choose field from measurement alice_temperature, or number from list:
0. Alice Temperature 4K
1. Alice Temperature 50K
2. Alice Temperature MXC
3. Alice Temperature Still
Name or Index: 1
```

Following this the program will prompt the user to do the following: Enter in a name, this name should simply be a unique identifier of which measurement field is being used to query the Influx DB data. The name should not include identifiers biased on which type of alert it is, i.e. if it is a critical alert or warning alert or if it is an upper bounded or lower bounded alert these will automatically be added by the program. For example in this case the name "Alice 50 K Temperature" was used and the final name of the alert that will be "Alice 50 K Temperature Upper Critical Alert".

The program will also ask the user to specify if the alert should fire if no data is coming in; this should be set to "Alerts" only in the sinai in which no data coming in should trigger the alert. 

```
Enter name: Alice 50 K Temperature
State alert when NO DATA? ('OK'/'Alerting') OK
Configure dashboard-alert pair? ('y'/'n') y
```

If the user choses to configure an alert-dashboard pair then they will have to first chose a database, then a respective panel in which to display the alert on. Note that this is only for time-series panels and the panels configured to any other setting do not have the option to display alerts. 

```
Choose dashboard names, or number from list:
0. Alice Fridge Dashboard
1. Bob Fridge Dashboard
2. Lab Weather Dashboard
3. Main Lab Dashboard
4. Water Chiller Dashboard
Name or Index: 0

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

Once all of the above are completed the program will send the request to create the alert and then will display all of the alerts visible, included the one just created. In this case we have successfully created a Grafana alert titled "Alice 50 K Temperature Upper Critical Alert" which queries data from the Influx DB database "fridge_database", from the measurement "alice_temperature" and field "Alice Temperature 50K" which triggers the "critical" alert rule in Grafana when the threshold 999 is surpassed.

```
----------- Configurations -----------
Name: 'Fridge Cold'        | File Name: 'fridge_cold_config.json'      | Description: fridge cooling values
Name: 'Fridge Warm'        | File Name: 'fridge_warming_config.json'   | Description: fridge warming values
Name: 'Test'               | File Name: 'test_config.json'             | Description: alert api demo
Name: 'Pause Alerts'       | File Name: 'pause_config.json'            | Description: pausing all alerts
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Critical Alert'      | Threshold: Greater than 999          | State: ON
```

## Alert Naming System

Alerts are named in a way that allows for no repeats and allows both the program and user to identify which type of alert it is. This means that the alert name is what the program uses to create the different type of alerts and thus if an alert is created that does not follow this naming convention then it will result in incorrect alerts. Luckily this system is very simple to understand. 

To start take the name "Alice 50 K Temperature Upper Critical Alert", there are two parts to every name. First is the unique identifier which in this case is "Alice 50 K Temperature" that the user defines either in the `alert_config.json` file or directly from the command line when creating an alert from scratch. This name must be unique to the field which Influx DB queries.

Second is the autogenerated part which the program adds on to specify which type of alert it is, in this case that is "Upper Critical Alert". There are a total of four different types of alerts that can be created:

- Upper Critical Alert; the one used in the example above
- Upper Warning Alert
- Lower Warning Alert 
- Lower Critical Alert

The "Upper" or "Lower" key word tells the program whether to trigger when the value is greater or less then the threshold respectively. The "Critical" or "Warning" key word tells the program to create a "Critical" or "Warning" alert. Critical and Warning alerts differ in both the color which they are displayed on in the dashboard panel (Critical alerts are red/dark-red while Warning alerts are orange/dark-orange) and also which notification policy to trigger. 

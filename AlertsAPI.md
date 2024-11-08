# Alerts API

The alerts API is a command line tool designed to allow users to view, edit, create and delele alerts that are associated with Grafana and Influx DB. Alerts additionally have configuration files that store large lists of preconfigured alerts so the user can simply edit the configuration JSON instead of editing individual alerts. 

In order to use the alerts API the user must ssh onto the MaLab server. The simplest action one can perform with this tool is to simply view the status of the alerts and view which configration files are avalible. To do this simply invoke `alerts` in the command line as shown below.

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
Name: 'Test'                                             | File Name: 'test_config.json'
Name: 'Pause Alerts'                                     | File Name: 'pause_config.json'
-----------     Alerts     -----------
```

From the output we see that under the "Configurations" section there are the 3 configuration files shown; any file in the /IoT-Server/Alerts-API that ends with `config.json` will be automatically considered a configuration file. Additinoally there are no Alerts defined yet. 

Additionally there is another file, the `alerts_config.json` file which defines how each alert is set up; unless a user is adding an additional datasource this file should not be edited. 

## Setting Alert Configuration 

Most of what users will do is set different alert configurations. As described above all alert configurations can be viewed when invoking the `alerts` command. A typical alert configuration file is structured as shown below, in this example we are looking at the "Test" configuration file:

``` json
{
    "name":"Test",
    "alerts":
    [
        {
            "title":"Alice 50 K Temperature Upper Warning Alert",
            "threshold":50,
            "state":"ON"
        }
    ]
}
```

The user can edit the threshold (any float value) or state ("ON" or "OFF") section, the names of the alerts follow a specifc pattern that allows for no repeats and for the program to recognize properties of the alert. These should generally not be edited, refer to the Alerts Name Nomenclature section if so. In order to enable the configuration file type `alerts --config "<configuration name>"`. Below is an example with the "Test" configuration file. If no error occurs you should see an output with the new alerts configured. 

```
malab@maserver:~ $ alerts --config "Test"
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
Name: 'Test'                                             | File Name: 'test_config.json'
Name: 'Pause Alerts'                                     | File Name: 'pause_config.json'
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
```

## Deleting Alerts

To delete an alert type `alerts --delete "<alert name>"` into the command line. It is possible to delete multiple alerts at once; for example if one is intrested in deleting all alerts that contain the word "Warning" the following command can be invoked `alerts --delete "Warning"`. If the user is intrested in deleting every alert the following command can be invoked `alerts --delete "*"`. Below is an example of what deleting an alert would appear as.

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
Name: 'Test'                                             | File Name: 'test_config.json'
Name: 'Pause Alerts'                                     | File Name: 'pause_config.json'
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --delete "Alice 50 K Temperature Upper Warning Alert"
Are you sure you want to delete: 'Alice 50 K Temperature Upper Warning Alert'? It is irreversible! (Y/n) Y
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
Name: 'Test'                                             | File Name: 'test_config.json'
Name: 'Pause Alerts'                                     | File Name: 'pause_config.json'
-----------     Alerts     -----------
```

## Edit Alert Value

To edit a single alert value type `alerts --name "<alert name>" --threshold <new threshold value>` where the threshold value can be any floating point number. One can only edit one alert at a time. Below is an exmaple of what editing an alert would appear as.

```
malab@maserver:~ $ alerts
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
Name: 'Test'                                             | File Name: 'test_config.json'
Name: 'Pause Alerts'                                     | File Name: 'pause_config.json'
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 50           | State: ON
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $
malab@maserver:~ $ alerts --name "Alice 50 K Temperature Upper Warning Alert" --threshold 999.111
----------- Configurations -----------
Name: 'Fridge Cold'                                      | File Name: 'fridge_cold_config.json'
Name: 'Fridge Warm'                                      | File Name: 'fridge_warming_config.json'
Name: 'Test'                                             | File Name: 'test_config.json'
Name: 'Pause Alerts'                                     | File Name: 'pause_config.json'
-----------     Alerts     -----------
Name: 'Alice 50 K Temperature Upper Warning Alert'       | Threshold: Greater than 999.111      | State: ON
```

## Edit Alert State

To edit a the state of alerts type `alerts --name "<alert name>" --state "<new state value>"` where new state can only take values "ON" or "OFF". It is possible to edit the state of multiple alerts at once by passing in a string that is contained in the alerts you want to change. For example to set the state of all alerts containing the word "Warning" to "OFF" one would type the command `alerts --name "Warning" --state "OFF"`. Below shows an example of this. 

```
```

## Creating Alerts

Creating alerts are more invoed than simply editing or deleting them. The user can create new alerts by editing the configuraiton JSON to include additinoal alerts however there are only bounded . In order to create new alerts the user must have a familiarity of how the server stores and retrevis the data on grafana. This is further explined in teh README.md file. 

Assuming the reader understands the high level of 

## Alert Naming Nomenclature

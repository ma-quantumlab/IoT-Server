# Database Flow:

InfluxDB organizes time-series data using a hierarchical structure consisting of databases, measurements, and fields. A database serves as a container for related time-series data, while a measurement represents a specific collection of time-stamped data points (similar to a table in relational databases). Within each measurement, fields store the actual values being recorded, such as temperature, pressure, or humidity. Fields are key-value pairs where the key is the field name and the value is the associated data. This structure allows InfluxDB to efficiently store, query, and analyze large amounts of time-series data.

Below gives the structure of the Databases on the Raspberry Pi, me sure to update this when new Databases, Measurements or Felids are added or changed. The bolded phrases are the case sensitive values of interest.  

Fridges Database (**fridge_database**):

- Alice Temperature Measurements (**alice_temperature**)
    - 50 K Temperature (**Alice Temperature 50K**)
    - 4 K Temperature: (**Alice Temperature 4K**)
    - Still Temperature: (**Alice Temperature Still**)
    - MXC Temperature: (**Alice Temperature MXC**)

- Alice Pressure Measurements (**alice_pressure**)
    - Pressure OVC (**Alice Pressure OVC**)
    - Still Side Pressure (**Alice Pressure Still Side**)
    - CH4 Pressure (**Alice Pressure CH4**)
    - CH3 Pressure (**Alice Pressure CH3**)
    - Note CH4 Pressure (**Alice Pressure CH4**) is subtracted from the CH3 Pressure (**Alice Pressure CH3**) to return the Pressure differential across the trap (**Alice Pressure Differential Across Trap**)
    - Tank Pressure (**Alice Pressure Tank**)

- Alice Compressor Measurements (**alice_compressor**)
    - Water In (**Alice Compressor Water In**)
    - Water Out (**Alice Compressor Water Out**)
    - Oil Temperature (**Alice Compressor Oil Temperature**)
    - Error Status (**Alice Compressor Error Status**)

- Alice Flowmeter Measurement (**alice_flowmeter**)
    - Flowmeter (**Alice Flowmeter**)

- Bob Temperature Measurements (**bob_temperature**)
    - 50 K Temperature (**Bob Temperature 50K**)
    - 4 K Temperature (**Bob Temperature 4K**)
    - Still Temperature: (**Bob Temperature Still**)
    - MXC Temperature: (**Bob Temperature MXC**)

- Bob Pressure Measurements (**bob_pressure**)
    - Pressure OVC (**Bob Pressure OVC**)
    - Still Side Pressure (**Bob Pressure Still Side**)
    - CH4 Pressure (**Bob Pressure CH4**)
    - CH3 Pressure (**Bob Pressure CH3**)
    - Note CH4 Pressure (**Bob Pressure CH4**) is subtracted from the CH3 Pressure (**Bob Pressure CH3**) to return the Pressure differential across the trap (**Bob Pressure Differential Across Trap**)
    - Tank Pressure: **Bob Pressure Tank**

- Bob Compressor Measurements (**bob_compressor**)
    - Water In (**Bob Compressor Water In**)
    - Water Out (**Bob Compressor Water Out**)
    - Oil Temperature (**Bob Compressor Oil Temperature**)
    - Error Status (**Bob Compressor Error Status**)

- Bob Flowmeter Measurement (**bob_flowmeter**)
    - Flowmeter (**Bob Flowmeter**)

Lab Weather Database (**weather_database**):

- G41A Measurements (room_measurement): <-- **NO LONGER ACTIVE: Check DHT Sensors** 
    - Temperature (G41A Temperature) <-- **NO LONGER ACTIVE: Check DHT Sensor 2** 
    - Humidity (G41A Humidity) <-- **NO LONGER ACTIVE: Check DHT Sensor 2** 
    - Temperature (Lab Temperature) <-- **NO LONGER ACTIVE Check DHT Sensor 1** 
    - Humidity (Lab Humidity) <-- **NO LONGER ACTIVE: Check DHT Sensor 1** 

- Room Lab Measurements (**dht_sensor_1**)
    - Temperature (**DHT Sensor 1 Temperature**)
    - Humidity (**DHT Sensor 1 Humidity**)
    
- Room G41A Measurements (**dht_sensor_2**)
    - Temperature (**DHT Sensor 2 Temperature**)
    - Humidity (**DHT Sensor 2 Humidity**)

- Fridge Surrounding Measurements (**near_fridges**):
    - Temperature (**Fridges Surrounding Temperature**)
    - Humidity (**Fridges Surrounding Humidity**)

- Makeup Air Supply Measurement (**makeup_air_supply**):
    - Temperature (**Makeup Air Supply Temperature**)
    - Humidity (**Makeup Air Supply Humidity**)

- Lab Fan Coil Unit Measurement (**g41_fan_coil_unit**):
    - Temperature (**Lab Fan Coil Unit Temperature**)
    - Humidity (**Lab Fan Coil Unit Humidity**)

- G41A Fan Coil Unit Measurement (**g41a_fan_coil_unit**):
    - Temperature (**G41A Fan Coil Unit Temperature**)
    - Humidity (**G41A Fan Coil Unit Humidity**)

- Alice Mixture Tank Measurement (**alice_mixture_tank**): 
    - Temperature (**Alice Mixture Tank Temperature**)
    - Humidity (**Alice Mixture Tank Humidity**)

- Bob Mixture Tank Measurement (**bob_mixture_tank**):
    - Temperature (**Bob Mixture Tank Temperature**)
    - Humidity (**Bob Mixture Tank Humidity**)
 
- 

Water Chiller Database (**water_chiller_database**):
- Water Chiller Measurement (**water_chiller**)
    - Temperature In (**Water Chiller Temperature In**)
    - Pressure In (**Pressure In**)
    - Pressure Out (**Pressure Out**)
    - Pressure Differential (**Pressure Differential**)

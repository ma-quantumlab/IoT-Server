# Database Flow:

InfluxDB organizes time-series data using a hierarchical structure consisting of databases, measurements, and fields. A database serves as a container for related time-series data, while a measurement represents a specific collection of time-stamped data points (similar to a table in relational databases). Within each measurement, fields store the actual values being recorded, such as temperature, pressure, or humidity. Fields are key-value pairs where the key is the field name and the value is the associated data. This structure allows InfluxDB to efficiently store, query, and analyze large amounts of time-series data.

Below gives the structure of the Databases on the Raspberry Pi, me sure to update this when new Databases, Measurements or Felids are added or changed. The bolded phrases are the case sensitive values of interest.  

Fridges Database (**fridge_database**):

- Alice Temperature Measurements (**alice_temperature**)
    - **Alice Temperature 50K**
    - **Alice Temperature 4K**
    - **Alice Temperature Still**
    - **Alice Temperature MXC**

- Alice Pressure Measurements (**alice_pressure**)
    - **Alice Pressure OVC**
    - **Alice Pressure Still Side**
    - **Alice Pressure CH4**
    - **Alice Pressure CH3**
    - Note **Alice Pressure CH4** is subtracted from **Alice Pressure CH3** to return **Pressure Differential Across Trap**
    - **Alice Pressure Tank**

- Alice Compressor Measurements (**alice_compressor**)
    - **Alice Compressor Water In**
    - **Alice Compressor Water Out**
    - **Alice Compressor Oil Temperature**
    - **Alice Compressor Error Status**

- Bob Temperature Measurements (**bob_temperature**)
   - **Bob Temperature 50K**
   - **Bob Temperature 4K**
   - **Bob Temperature Still**
   - **Bob Temperature MXC**

- Bob Pressure Measurements (**bob_pressure**)
   - **Bob Pressure OVC**
   - **Bob Pressure Still Side**
   - **Bob Pressure CH4**
   - **Bob Pressure CH3**
   - Note **Bob Pressure CH4** is subtracted from **Bob Pressure CH3** to return **Pressure Differential Across Trap**
   - **Bob Pressure Tank**

- Bob Compressor Measurements (**bob_compressor**)
   - **Bob Compressor Water In**
   - **Bob Compressor Water Out**
   - **Bob Compressor Oil Temperature**
   - **Bob Compressor Error Status**

Lab Weather Database (****):

- 

Water Chiller Database (****):

-



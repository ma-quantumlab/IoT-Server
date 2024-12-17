let output = {};
let keyToLabelMap = {
    // Fridges
    'bob_temp_50k': { label: 'Bob Temperature 50K', groupIndex: 0 },
    'bob_temp_4k': { label: 'Bob Temperature 4K', groupIndex: 0 },
    'bob_temp_still': { label: 'Bob Temperature Still', groupIndex: 0 },
    'bob_temp_mxc': { label: 'Bob Temperature MXC', groupIndex: 0 },
    // Fridges
    'bob_pressure_ovc': { label: 'Bob Pressure OVC', groupIndex: 1 },
    'bob_pressure_still': { label: 'Bob Pressure Still Side', groupIndex: 1 },
    'bob_pressure_diff_ch4': { label: 'Bob Pressure CH4', groupIndex: 1 },
    'bob_pressure_diff_ch3': { label: 'Bob Pressure CH3', groupIndex: 1 },
    'bob_pressure_tank': { label: 'Bob Pressure Tank', groupIndex: 1 },
    // Fridges
    'bob_compressor_water_in': { label: 'Bob Compressor Water In', groupIndex: 2 },
    'bob_compressor_water_out': { label: 'Bob Compressor Water Out', groupIndex: 2 },
    'bob_compressor_oil_temp': { label: 'Bob Compressor Oil Temperature', groupIndex: 2 },
    'bob_compressor_err': { label: 'Bob Compressor Error Status', groupIndex: 2 },
    // Fridges
    'alice_temp_50k': { label: 'Alice Temperature 50K', groupIndex: 3 },
    'alice_temp_4k': { label: 'Alice Temperature 4K', groupIndex: 3 },
    'alice_temp_still': { label: 'Alice Temperature Still', groupIndex: 3 },
    'alice_temp_mxc': { label: 'Alice Temperature MXC', groupIndex: 3 },
    // Fridges
    'alice_pressure_ovc': { label: 'Alice Pressure OVC', groupIndex: 4 },
    'alice_pressure_still': { label: 'Alice Pressure Still Side', groupIndex: 4 },
    'alice_pressure_diff_ch4': { label: 'Alice Pressure CH4', groupIndex: 4 },
    'alice_pressure_diff_ch3': { label: 'Alice Pressure CH3', groupIndex: 4 },
    'alice_pressure_tank': { label: 'Alice Pressure Tank', groupIndex: 4 },
    // Fridges
    'alice_compressor_water_in': { label: 'Alice Compressor Water In', groupIndex: 5 },
    'alice_compressor_water_out': { label: 'Alice Compressor Water Out', groupIndex: 5 },
    'alice_compressor_oil_temp': { label: 'Alice Compressor Oil Temperature', groupIndex: 5 },
    'alice_compressor_err': { label: 'Alice Compressor Error Status', groupIndex: 5 },
    // Lab Weather
    'g41a_temp': { label: 'G41A Temperature', groupIndex: 6 },
    'g41a_hum': { label: 'G41A Humidity', groupIndex: 6 },
    'lab_temp': { label: 'Lab Temperature', groupIndex: 6 },
    'lab_hum': { label: 'Lab Humidity', groupIndex: 6 },
    // Lab Weather
    'fridges_temp': { label: 'Fridges Surrounding Temperature', groupIndex: 7 },
    'fridges_hum': { label: 'Fridges Surrounding Humidity', groupIndex: 7 },
    // Lab Weather
    'lab_makeup_as_temp': { label: 'Makeup Air Supply Temperature', groupIndex: 8 },
    'lab_makeup_as_hum': { label: 'Makeup Air Supply Humidity', groupIndex: 8 },
    // Lab Weather
    'lab_fcu_temp': { label: 'Lab Fan Coil Unit Temperature', groupIndex: 9 },
    'lab_fcu_hum': { label: 'Lab Fan Coil Unit Humidity', groupIndex: 9 },
    // Lab Weather
    'g41a_fcu_temp': { label: 'G41A Fan Coil Unit Temperature', groupIndex: 10 },
    'g41a_fcu_hum': { label: 'G41A Fan Coil Unit Humidity', groupIndex: 10 },
    // Lab Weather
    'mix_alice_temp': { label: 'Alice Mixture Tank Temperature', groupIndex: 11 },
    'mix_alice_hum': { label: 'Alice Mixture Tank Humidity', groupIndex: 11 },
    // Lab Weather
    'mix_bob_temp': { label: 'Bob Mixture Tank Temperature', groupIndex: 12 },
    'mix_bob_hum': { label: 'Bob Mixture Tank Humidity', groupIndex: 12 },
    // Water Chiller
    'temp_in': { label: 'Water Chiller Temperature In', groupIndex: 13 },
    'pressure_in': { label: 'Pressure In', groupIndex: 13 },
    'pressure_out': { label: 'Pressure Out', groupIndex: 13 },
    'pressure_diff': { label: 'Pressure Differential', groupIndex: 13 },
    // Fridges Cont. 
    'bob_flowmeter': { label: 'Bob Flowmeter', groupIndex: 14 },
    'alice_flowmeter' : {label : 'Alice Flowmeter', groupIndex: 15}
};

let resultArray = new Array(16).fill(null); 

let foundIndex = -1;

for (let key in msg.payload) {
    if (keyToLabelMap.hasOwnProperty(key)) {
        let fieldInfo = keyToLabelMap[key];
        output[fieldInfo.label] = msg.payload[key];
        foundIndex = fieldInfo.groupIndex;
    }
}

if (foundIndex !== -1) {
    resultArray[foundIndex] = { payload: output };
}

return resultArray;

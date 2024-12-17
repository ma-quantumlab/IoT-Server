let devices = [
    { 
        index: 0, 
        fields: ['bob_temp_50k', 'bob_temp_4k', 'bob_temp_still', 'bob_temp_mxc'], 
        labels: ['Bob Temperature 50K', 'Bob Temperature 4K', 'Bob Temperature Still', 'Bob Temperature MXC']
    },
    { 
        index: 1, 
        fields: ['bob_pressure_ovc', 'bob_pressure_still', 'bob_pressure_diff_ch4', 'bob_pressure_diff_ch3', 'bob_pressure_tank'], 
        labels: ['Bob Pressure OVC', 'Bob Pressure Still Side', 'Bob Pressure CH4', 'Bob Pressure CH3', 'Bob Pressure Tank']
    },
    { 
        index: 2, 
        fields: ['bob_compressor_water_in', 'bob_compressor_water_out', 'bob_compressor_oil_temp', 'bob_compressor_err'], 
        labels: ['Bob Compressor Water In', 'Bob Compressor Water Out', 'Bob Compressor Oil Temperature', 'Bob Compressor Error Status']
    },
    { 
        index: 3, 
        fields: ['alice_temp_50k', 'alice_temp_4k', 'alice_temp_still', 'alice_temp_mxc'], 
        labels: ['Alice Temperature 50K', 'Alice Temperature 4K', 'Alice Temperature Still', 'Alice Temperature MXC']
    },
    { 
        index: 4, 
        fields: ['alice_pressure_ovc', 'alice_pressure_still', 'alice_pressure_diff_ch4', 'alice_pressure_diff_ch3', 'alice_pressure_tank'], 
        labels: ['Alice Pressure OVC', 'Alice Pressure Still Side', 'Alice Pressure CH4', 'Alice Pressure CH3', 'Alice Pressure Tank']
    },
    { 
        index: 5, 
        fields: ['alice_compressor_water_in', 'alice_compressor_water_out', 'alice_compressor_oil_temp', 'alice_compressor_err'], 
        labels: ['Alice Compressor Water In', 'Alice Compressor Water Out', 'Alice Compressor Oil Temperature', 'Alice Compressor Error Status']
    },
    { 
        index: 6, 
        fields: ['g41a_temp', 'g41a_hum', 'lab_temp', 'lab_hum'], 
        labels: ['G41A Temperature', 'G41A Humidity', 'Lab Temperature', 'Lab Humidity']
    },
    { 
        index: 7, 
        fields: ['fridges_temp', 'fridges_hum'], 
        labels: ['Fridges Surrounding Temperature', 'Fridges Surrounding Humidity']
    },
    { 
        index: 8, 
        fields: ['lab_makeup_as_temp', 'lab_makeup_as_hum'], 
        labels: ['Makeup Air Supply Temperature', 'Makeup Air Supply Humidity']
    },
    { 
        index: 9, 
        fields: ['lab_fcu_temp', 'lab_fcu_hum'], 
        labels: ['Lab Fan Coil Unit Temperature', 'Lab Fan Coil Unit Humidity']
    },
    { 
        index: 10, 
        fields: ['g41a_fcu_temp', 'g41a_fcu_hum'], 
        labels: ['G41A Fan Coil Unit Temperature', 'G41A Fan Coil Unit Humidity']
    },
    { 
        index: 11, 
        fields: ['mix_alice_temp', 'mix_alice_hum'], 
        labels: ['Alice Mixture Tank Temperature', 'Alice Mixture Tank Humidity']
    },
    { 
        index: 12, 
        fields: ['mix_bob_temp', 'mix_bob_hum'], 
        labels: ['Bob Mixture Tank Temperature', 'Bob Mixture Tank Humidity']
    },
    { 
        index: 13, 
        fields: ['temp_in', 'pressure_in', 'pressure_out', 'pressure_diff'], 
        labels: ['Water Chiller Temperature In', 'Pressure In', 'Pressure Out', 'Pressure Differential']
    },
    { 
        index: 14, 
        fields: ['bob_flowmeter'], 
        labels: ['Bob Flowmeter']
    },
    { 
        index: 15, 
        fields: ['alice_flowmeter'], 
        labels: ['Alice Flowmeter']
    }
];

let resultArray = new Array(16).fill(null);
let output = {};

// Map payload fields to correct labels dynamically
for (let device of devices) {
    let groupOutput = {};
    for (let i = 0; i < device.fields.length; i++) {
        let field = device.fields[i];
        let label = device.labels[i];

        if (msg.payload.hasOwnProperty(field)) {
            groupOutput[label] = msg.payload[field];
        }
    }

    if (Object.keys(groupOutput).length > 0) {
        resultArray[device.index] = { payload: groupOutput };
    }
}

return resultArray;

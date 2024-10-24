def get_value(mqtt_subsection, today):
    from Log_watcher import DataSource, log_root, index

    path = log_root + today + "\\" + "maxigauge " + today + ".log"

    #if os.not os.path.exists(path):
        #return None

    lastline = DataSource.get_last_line(path).rsplit(",")
    timestamp = lastline[0] + "," + lastline[1]
    
    if (mqtt_subsection == "alice_pressure_ovc"):
        return (timestamp, float(lastline[index(lastline, "CH1")+3])) # CH 1
    elif (mqtt_subsection == "alice_pressure_still"):
        return (timestamp, float(lastline[index(lastline, "CH2")+3])) # CH 2
    elif (mqtt_subsection == "alice_pressure_diff_ch4"):
        return (timestamp, float(lastline[index(lastline, "CH4")+3])) # CH 4
    elif (mqtt_subsection == "alice_pressure_diff_ch3"):
        return (timestamp, float(lastline[index(lastline, "CH3")+3])) # CH 3
    elif (mqtt_subsection == "alice_pressure_tank"):
        return (timestamp, float(lastline[index(lastline, "CH5")+3])) # CH 5
    raise Exception(f"'{mqtt_subsection}' is not a valid request")
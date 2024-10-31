import os

def get_value(mqtt_subsection, today, required):
    from Log_watcher import DataSource, log_root

    channel = ""
    if "temp_50k" in mqtt_subsection: 
        channel = "CH1"
    elif "temp_4k" in mqtt_subsection:
        channel = "CH2"
    elif "temp_still" in mqtt_subsection:
        channel = "CH5"
    elif "temp_mxc" in mqtt_subsection:
        channel = "CH6"
       
    path = log_root + today + "\\" + channel + " T " + today + ".log"

    if not os.path.exists(path) and not required: # Channels may not be present due to Bluefors Config
        return None

    lastline = DataSource.get_last_line(path).rsplit(",")
    timestamp = lastline[0] + "," + lastline[1]
    
    return (timestamp, float(lastline[2]))
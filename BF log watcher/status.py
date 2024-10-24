def get_value(mqtt_subsection, today, required):

    from Log_watcher import DataSource, log_root, index
    
    path = log_root + today + "\\" + "Status_" + today + ".log"

    #if not os.path.exists(path):
        #return None

    lastline = DataSource.get_last_line(path).rsplit(",")
    timestamp = lastline[0] + "," + lastline[1]
    
    if "compressor_err" in mqtt_subsection: 
        return (timestamp, float(lastline[index(lastline, "cpaerr")+1])) # cpaerr
    elif "compressor_water_in" in mqtt_subsection:
        return (timestamp, float(lastline[index(lastline, "cpatempwi")+1])) # cpatempwi
    elif "compressor_water_out" in mqtt_subsection:
        return (timestamp, float(lastline[index(lastline, "cpatempwo")+1])) # cpatempwo
    elif "compressor_oil_temp" in mqtt_subsection:
        return (timestamp, float(lastline[index(lastline, "cpatempo")+1])) # cpatempo
    raise Exception(f"'{mqtt_subsection}' is not a valid request")
def get_value(mqtt_subsection, today, required):
    from Log_watcher import DataSource, log_root


    path = log_root + today + "\\" + "Flowmeter " + today + ".log"

    lastline = DataSource.get_last_line(path)
    timestamp = lastline.rsplit(",")[0] + "," + lastline.rsplit(",")[1]

    return (timestamp, float(lastline.rsplit(",")[2]))
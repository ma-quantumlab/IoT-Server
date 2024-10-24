from Log_watcher import log_root, get_last_line

def get_value(mqtt_subsection, today):

    path = log_root + today + "\\" + "Flowmeter " + today + ".log"

    lastline = get_last_line(path)
    timestamp = lastline.rsplit(",")[0] + "," + lastline.rsplit(",")[1]

    return (timestamp, float(lastline.rsplit(",")[2]))
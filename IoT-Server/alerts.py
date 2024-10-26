#! bin/python

"""
Created by: Dhruv Upreti
Ma Lab Quantum Group
"""

from dotenv import load_dotenv 
import requests
import argparse
import json
import sys
import os

BLUE = "\033[94m"
GREEN = "\033[92m"
RESET = "\033[0m"

load_dotenv()

grafana_token = os.getenv("GRAPHANA_TOKEN")
grafana_url = "http://192.168.1.104:3000/"
infludb_url = "http://192.168.1.104:8086/"

provisioning_header = {
    "Content-Type":"application/json",
    "Authorization":f"Bearer {grafana_token}"
}

datasource_header = {
    "Content-Type":"application/json",
    "Application":"application/json",
    "Authorization":f"Bearer {grafana_token}"
}

influx_db_get_measurements_header = lambda database_name : {
    "db": database_name,
    "q": "SHOW MEASUREMENTS"
}

influxdb_get_fields_header = lambda database_name, measurement_name : {
    "db": database_name,
    "q": f"SHOW FIELD KEYS FROM {measurement_name}" 
}

alert_rules_url = "api/v1/provisioning/alert-rules/"
dashboard_url = "api/dashboards/uid/"
update_dashboard_url = "api/dashboards/db/"
datasource_url = "api/datasources/"
query_url = "query/"
search_url = "api/search/"

main_folder_uid = "c647d423-8003-4ae5-b26a-8495098f82b2"
rule_group = "10 Sec Evaluation Group"

class Threshold:
    thresholds  = []

    def __init__(self, alertJson):
        self.alertJson = alertJson

    def __del__(self): # Deletes dashboard thresholds, alert from api, etc.
        self.removeDashboardThreshold()
        httpDeleteRequest()

    def __str__(self): # Prints status of threshold to command line 
        return f"Name: {BLUE}{self.getName():<{50}}{RESET} | Value: {GREEN}{self.getThreshold():<{15}}{RESET} | Silenced: {GREEN}{self.getStateString():<{20}}{RESET}"

    def getName(self): # Returns title of Alert
        return self.alertJson["title"] 

    def getThreshold(self): # Returns numerical value of Alert
        return self.alertJson["data"][2]["model"]["conditions"][0]["evaluator"]["params"][0]

    def getStateString(self): # Return 'True' or 'False' state of Alert
        return "True" if self.alertJson["isPaused"] else "False"

    def getAnnotatedDashboardUid(self): # returns Uid of dashboard associated with Alert
        return self.alertJson["annotations"]["__dashboardUid__"]

    def getAlertId(self): # Returns Alert Uid
        return self.alertJson["uid"]
    
    def getDatasourceUid(self): # Returns the Uid of the Data source, i.e. which Influx DB database 
        return self.alertJson["data"][Threshold.getJsonArrayIndex("refId", self.alertJson["data"], "A")[0]]["datasourceUid"]

    def getMeasurement(self): # Returns name of measurement from Influx DB database 
        return self.alertJson["data"][Threshold.getJsonArrayIndex("refId", self.alertJson["data"], "A")[0]]["measurement"]
    
    def getFeild(self): # Returns name of Feild from Influx DB measurement
        a_refId_index = Threshold.getJsonArrayIndex("refId", self.alertJson["data"], "A")[0]
        feild_type_index = Threshold.getJsonArrayIndex("type", self.alertJson["data"][a_refId_index]["select"][0], "field")
        return self.alertJson["data"][a_refId_index]["select"][0][feild_type_index]["params"][0]
    
    def getAllDashboardPanels(self): # Returns tuple list of dashboard Uid and associated panel number
        dashboardPanels = []
        for dashboard in Threshold.getDashboards().values():
            for panel in httpGetRequest(grafana_url+dashboard_url+dashboard["uid"])["dashboard"]["panels"]:
                if self.checkPanelMatch(panel):
                    dashboardPanels.append(dashboard, panel["num"])
    
        return dashboardPanels
    
    def checkPanelMatch(self, panel): # Checks to see if datasource parameters match for a dashboard panel
        return panel["targets"][0]["datasource"]["uid"] == self.getDatasourceUid() \
            and panel["targets"][0]["measurement"] == self.getMeasurement() \
            and panel["targets"][0]["select"][0][Threshold.getJsonArrayIndex("type", panel["targets"][0]["select"][0], "field")]["params"][0] == self.getFeild()
    
    def setThresholdValue(self, value):
        self.alertJson["data"][2]["model"]["conditions"][0]["evaluator"]["params"][0] = value
        httpPutRequest(alert_rules_url+self.getAlertId(), self.alertJson)

    def createDashboardThreshold(self): # Create threshold in dashboard from alertJson value, shift other values if required
        for dashboardId, panelNum in self.getAllDashboardPanels().items():

            dashboardJson = json.loads(httpGetRequest(grafana_url+dashboard_url+dashboardId))
            color_indices = lambda color : Threshold.getJsonArrayIndex("color", dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"], color)
            value = self.getThreshold()

            if "Upper" in self.getName():
                if "Warning" in self.getName():
                    dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].append({"color":"orange", "value":value})                    
                else:
                    dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].append({"color":"red", "value":value})
            else:
                if "Warning" in self.getName():
                    dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"][color_indices("green")]["color"] = "dark-orange"
                    dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].append({"color":"green", "value":value})
                else:
                    if Threshold.getJsonArrayIndex("color", dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"], "dark-orange"):
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"][color_indices("dark-orange")]["color"] = "dark-red"
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].append({"color":"dark-orange", "value":value})
                    else:
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"][color_indices("green")]["color"] = "dark-red"
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].append({"color":"green", "value":value})

            httpPostRequest(grafana_url+update_dashboard_url, dashboardJson)
        
    def removeDashboardThreshold(self): # Delete threshold in dashboard, shift other values if required 
        for dashboardId, panelNum in self.getAllDashboardPanels().items():

            dashboardJson = json.loads(httpGetRequest(grafana_url+dashboard_url+dashboardId))
            color_indices = lambda color : Threshold.getJsonArrayIndex("color", dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"], color)

            if "Upper" in self.getName():
                dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].pop(color_indices("orange" if "Warning" in self.getName else "red"))                    
            else:
                if "Warning" in self.getName():
                    dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].pop(color_indices("green"))
                    dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"][color_indices("dark-orange")]["color"] = "green"
                else:
                    if Threshold.getJsonArrayIndex("color", dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"], "dark-orange"):
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].pop(color_indices("dark-orange"))
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"][color_indices("dark-red")]["color"] = "dark-orange"
                    else:
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"].pop(color_indices("green"))
                        dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"][color_indices("dark-red")]["color"] = "green"

            httpPostRequest(grafana_url+update_dashboard_url, dashboardJson)
        
    def changeDashboardThreshold(self, value, editAlertJson=True): # Change the value of the dashboard threshold 

        if editAlertJson is True:
            self.setThresholdValue(self, value)

        for dashboardId, panelNum in self.getAllDashboardPanels().items():

            thresholdNum = None
            dashboardJson = json.loads(httpGetRequest(grafana_url+dashboard_url+dashboardId))

            color_indices = lambda color : Threshold.getJsonArrayIndex("color", dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"], color)

            if "Warning" in self.getName() and "Upper" in self.getName():
                thresholdNum = color_indices("orange")[0]
            elif "Critical" in self.getName() and "Upper" in self.getName():
                thresholdNum = color_indices("red")[0]
            elif "Warning" in self.getName() and "Lower" in self.getName():
                thresholdNum = color_indices("green")[0]
            elif "Critical" in self.getName() and "Lower" in self.getName():
                if Threshold.getJsonArrayIndex("color", dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"], "dark-orange", True):
                    thresholdNum = color_indices("dark-orange")[0]
                else:
                    thresholdNum = color_indices("green")[0]

            dashboardJson["dashboard"]["panels"][panelNum]["fieldConfig"]["defaults"]["thresholds"]["steps"][thresholdNum]["value"] = value

            httpPostRequest(grafana_url+update_dashboard_url, dashboardJson)

    def changeDashboardThresholdState(self, state): # Sets the state of the dashboard's threshold
        if state == "ON":
            self.alertJson["isPaused"] = bool(False)
            self.createDashboardThreshold()

        elif state == "OFF":
            self.alertJson["isPaused"] = bool(True)
            self.removeDashboardThreshold()

        else:
            raise Exception(f"\"{state}\" not a valid state, must be \"ON\" or \"OFF\"")

        httpPutRequest(alert_rules_url+self.getAlertId(), self.alertJson)

    @staticmethod
    def createAlert(threshold, state, bound_type, alert_type):
        print(f"Creating alert ... Enter in values below:")
            
        databases = {database["name"]:database["uid"] for database in httpGetRequest(grafana_url+datasource_url, datasource_header)}
        database = Threshold.getCheck("Influx DB databases", databases.keys)

        measurements = httpGetRequest(infludb_url+query_url, influx_db_get_measurements_header(database))['results'][0]['series'][0]['values']
        measurement = Threshold.getCheck(f"measurement from database {database}", measurements)

        fields = [field[0] for field in httpGetRequest(infludb_url+query_url, influxdb_get_fields_header(database, measurement))['results'][0]['series'][0]['values']]
        field = Threshold.getCheck(f"field from measurement {measurement}", fields)

        with open('alert_template.json', 'r') as file:
            alert_template = json.loads(file)

            alert_template["ruleGroup"] = rule_group
            alert_template["folderUID"] = main_folder_uid
            alert_template["title"] = input("Enter name: ") + "Upper " if bound_type == "gt" else "Lower " + alert_type + "Alert" 

            a_refId_index = Threshold.getJsonArrayIndex("refId", alert_template["data"], "A")[0]
            c_refId_index = Threshold.getJsonArrayIndex("refId", alert_template["data"], "C")[0]

            alert_template["data"][a_refId_index]["datasourceUid"] = databases[database]
            alert_template["data"][a_refId_index]["model"]["datasource"]["uid"] = databases[database]
            alert_template["data"][a_refId_index]["measurement"] = measurement

            feild_type_index = Threshold.getJsonArrayIndex("type", alert_template["data"][a_refId_index]["select"][0], "field")
            alert_template["data"][a_refId_index]["select"][0][feild_type_index]["params"][0] = field
            alert_template["data"][a_refId_index]["select"][0][feild_type_index]["type"] = bound_type

            alert_template["data"][c_refId_index]["model"]["conditions"][0]["evaluator"]["params"][0] = threshold

            alert_template["noDataState"] = strictInput("State alert when NO DATA? ('OK'/'Alerting')", ["OK", "Alerting"])

            if strictInput("Configure dashboard-alert pair? ('y'/'n')", ["y", "n"]) == "y":
                dashboards = Threshold.getDashboards()
                alert_template["annotations"]["__dashboardUid__"] = dashboards[Threshold.getCheck("dashboard names ", dashboards.keys())]
                alert_template["annotations"]["__panelId__"] = input("Enter in panel ID ,resolve this") # TODO Resolve this err
                
            if state == "ON":
                alert_template["isPaused"] = bool(False)
            elif state == "OFF":
                alert_template["isPaused"] = bool(True)
            else:
                raise Exception(f"State {state} must be 'ON' or 'OFF'")

            alert = Threshold(alert_template)
            alert.createDashboardThreshold()
            Threshold.thresholds.append(alert)            
            return alert

    @staticmethod
    def getJsonArrayIndex(subfield, json, value, empty=False):
        arrIndices = []
        for index, subJson in enumerate(json):
            if value == subJson[subfield]:
                arrIndices.append(index)
                break

        if len(arrIndices) == 0 and not empty:
            raise Exception(f"{value} is not found in Json Array {json}")
        return arrIndices

    @staticmethod
    def getThresholdFromName(name, multipleThresholds=False):
        result = []
        for threshold in Threshold.thresholds:
            if name in threshold.getName():
                result.append(threshold)

        if result is []:
            return None
        return result if multipleThresholds else result[0]

    @staticmethod
    def removeDescriptors(string):
        return string.replace("Warning", "").replace("Critical", "").replace("Alert", "").replace("Upper").replace("Lower").rstrip()
    
    @staticmethod
    def getDashboards(): # Gets all dashboards on grafana 
        dashboardUids = {}
        for dashboard in httpGetRequest(grafana_url+search_url):
            if dashboard["type"] != "dash-db":
                continue
            dashboardUids[dashboard["title"]] = dashboard["uid"]

        return dashboardUids
    
    @staticmethod
    def getCheck(parameterName, parameters):
        print(f"Choose {parameterName}, or number from list:")
        print("\n".join(f"{index}. {parameter}" for index, parameter in enumerate(parameters)))
        
        parameter = input("Name or Index: ")

        while True:
            if parameter in parameters:
                return parameter
            elif parameter.isdigit() and int(parameter) < len(parameters):
                return parameters[parameter]
            else:
                parameter = input(f"'{parameter}' not in {parameterName} list or in range of possible indexes, retry: ")

def httpGetRequest(url, header=provisioning_header):
    request = requests.get(url, headers=header)
    if request.status_code != 200:
        raise Exception(f"Error in request GET: {json.dumps(request.json())}")
    return json.dumps(request.json())

def httpPutRequest(url, jsonMessage, header=provisioning_header):
    request = requests.put(url, data=json.dumps(jsonMessage), headers=header)
    if request.status_code != 200:
        raise Exception(f"Error in request PUT: {json.dumps(request.json())}")
    return json.dumps(request.json())

def httpPostRequest(url, jsonMessage, header=provisioning_header):
    request = requests.post(url, data=json.dumps(jsonMessage), headers=header)
    if request.status_code != 200:
        raise Exception(f"Error in request POST: {json.dumps(request.json())}")
    return json.dumps(request.json())

def httpDeleteRequest(url, jsonMessage, header=provisioning_header):
    request = requests.delete(url, data=json.dumps(jsonMessage), headers=header)
    if request.status_code != 200:
        raise Exception(f"Error in request DELETE: {json.dumps(request.json())}")
    return json.dumps(request.json())

def strictInput(question, correctValues):
    while True:
        answer = input(question)
        if answer in correctValues:
            return answer
        else:
            print(f"Incorrect value: {answer}, enter correct value: '{', '.join(correctValues)}'")
    
def getArguments():
    parser = argparse.ArgumentParser(description='edit and view threshold values')

    parser.add_argument("--name", default=None, type=str, help="enter EXACT threshold name, to view names run program w/o arguments")
    parser.add_argument("--threshold", default=None, type=float, help="float value for threshold")
    parser.add_argument("--state", default=None, type=str, help="'ON' or 'OFF'")
    parser.add_argument("--create_upper_critical", action="store_true", help="create critical upper bound alert")
    parser.add_argument("--create_lower_critical", action="store_true", help="create critical lower bound alert")
    parser.add_argument("--create_upper_warning", action="store_true", help="create warning upper bound alert")
    parser.add_argument("--create_lower_warning", action="store_true", help="create warning lower bound alert")
    parser.add_argument("--delete", action="store_true", type=str, help="delete alert")
    parser.add_argument("--json", default=None, type=str, help="debug only")

    return parser.parse_args()

if __name__ == "__main__":
    try:
        arguments = getArguments()

        alerts = json.loads(httpGetRequest(grafana_url+alert_rules_url))

        for alert in alerts:
            Threshold.thresholds.append(Threshold(alert))

        if arguments.create_upper_critical is not None ^ arguments.create_upper_warning is not None ^ \
           arguments.create_lower_critical is not None ^ arguments.create_lower_warning ^ \
           arguments.delete is not None and arguments.threshold and arguments.state:
            if arguments.create_upper_critical:                
                Threshold.thresholds.append(Threshold.createAlert(arguments.threshold, arguments.state, "gt", "Critical"))
            elif arguments.create_lower_critical:
                Threshold.thresholds.append(Threshold.createAlert(arguments.threshold, arguments.state, "lt", "Critical"))
            elif arguments.create_upper_warning:
                Threshold.thresholds.append(Threshold.createAlert(arguments.threshold, arguments.state, "lt", "Warning"))
            elif arguments.create_lower_warning:
                Threshold.thresholds.append(Threshold.createAlert(arguments.threshold, arguments.state, "gt", "Warning"))

            elif arguments.delete and len(Threshold.getThresholdFromName(arguments.delete)) == 1:
                confirmation = strictInput(f"Are you sure you want to delete: '{arguments.delete}' (Y/n)", ["Y", "n"])
                if confirmation == "Y":
                    for index, threshold in enumerate(Threshold.thresholds):
                        if threshold.getName() == arguments.delete:
                            del Threshold.thresholds[index]
                    quit()
                else:
                    quit()
            else:
                quit()
                
        if arguments.name is not None:
            if arguments.threshold is not None and arguments.state is not None:
                raise Exception("Edit one property per request")

            if arguments.threshold is not None:
                threshold = Threshold.getThresholdFromName(arguments.name)
                if threshold is None:
                    raise Exception(f"Threshold {arguments.name} does not exist")
                if threshold.getStateString() == "False":
                    threshold.changeDashboardThresholdState(arguments.threshold)
                else:
                    threshold.setThresholdValue(arguments.threshold)

            if arguments.state is not None:
                thresholds = Threshold.getThresholdFromName(arguments.name, True)
                if thresholds is None:
                    raise Exception(f"Threshold {arguments.name} does not exist")
                for threshold in thresholds:
                    threshold.changeDashboardThresholdState(arguments.state)

            if "alert" in arguments.json:
                print(httpGetRequest(dashboard_url+Threshold.getThresholdFromName(arguments.name).getAlertId()))
                quit()

            if "dashboard" in arguments.json:
                print(httpGetRequest(dashboard_url+Threshold.getThresholdFromName(arguments.name).getDashboardId()))
                quit()

        for enum, threshold in enumerate(json.loads(httpGetRequest(grafana_url+alert_rules_url))):
            Threshold.thresholds[enum] = Threshold(threshold)
            print(Threshold(threshold))

    except Exception as exception:
        if "Error in request" in str(exception):
            print(f"ERROR in request: {str(exception)}")
            print("Rerunning Program ... ")

            python = sys.executable
            os.execv(python, [python] + sys.argv)
        else:
            raise exception
        
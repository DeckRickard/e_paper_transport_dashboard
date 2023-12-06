#!/usr/bin/python
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import requests
from requests.auth import HTTPBasicAuth
import json

logging.basicConfig(level=logging.DEBUG)

@dataclass
class Stop(object):
    name: str
    type: str
    code: str

@dataclass
class Arrival(object):
    line: str
    destination: str
    time_to_arrival: int
    formatted_arrival_time: str

@dataclass
class DepartureBoard(object):
    station_name: str
    station_code: str
    departures: list

def get_bus_arrival_predictions(stop_id):
    logging.info(f"Pulling arrival info for {stop_id}.")
    url = f"https://api.tfl.gov.uk/StopPoint/{stop_id}/Arrivals"

    request = requests.get(url)
    data = request.json()
    arrivals = []

    for prediction in data:
        arrivals.append(Arrival(prediction["lineName"], prediction["destinationName"], prediction["timeToStation"], format_predicted_time(prediction["timeToStation"])))
    
    arrivals.sort(key=lambda x: x.time_to_arrival, reverse=False) # This sorts the list in ascending order by arrival time.
    return arrivals

def format_predicted_time(arrival_time):
    arrival_minutes = int(arrival_time / 60)

    if arrival_minutes == 0:
        return "due"
    elif arrival_minutes < 30: # Predicted arrivals sooner than 30 minutes are displayed as minutes, longer than that will display a timestamp.
        return str(arrival_minutes)
    else:
        current_time = datetime.now()
        return (current_time + timedelta(minutes=arrival_minutes)).strftime('%H:%M')

def get_bus_stop_information(stop_id):
    logging.info(f"Pulling stop details for {stop_id}")
    url = f"https://api.tfl.gov.uk/StopPoint/{stop_id}"

    request = requests.get(url)
    data = request.json()
    stop_name = data["commonName"]
    child_stop = find_child_stop(data["children"], stop_id)
    stop_type = child_stop["modes"][0]
    stop_code = child_stop["stopLetter"]
    return Stop(stop_name, stop_type, stop_code)

def find_child_stop(children, stop_id): # TfL supplies a list of children for specific bus stops, etc. We need to find the correct child from the StopPoint data.
    child_ids = [child["naptanId"] for child in children]
    child_index = child_ids.index(stop_id)
    return children[child_index]

def get_train_departure_board(station_id):
    logging.info(f"Pulling details for train station ID: {station_id}")
    url = f"https://api.rtt.io/api/v1/json/search/{station_id}"

    with open("./settings.json") as file:
            settings = json.load(file)["transport"]

    user = settings["RTT_api_user"]
    password = settings["RTT_api_pass"]
    request = requests.get(url, auth=(user, password))
    data = request.json()
    
    station_name = data["location"]["name"]
    station_code = data["location"]["crs"]
    departures = []
    if not data["services"]:
        return DepartureBoard(station_name, station_code, []) 
    
    for arrival in data["services"]:
        operator_name = arrival["atocName"]
        destination = arrival["locationDetail"]["destination"][0]["description"]
        unformatted_departure_time = arrival["locationDetail"]["realtimeDeparture"]
        formatted_departure_time = f"{unformatted_departure_time[:2]}:{unformatted_departure_time[2:]}"
        
        departures.append(Arrival(operator_name, destination, None, formatted_departure_time))

    return DepartureBoard(station_name, station_code, departures)


if __name__ == "__main__":
    # These functions used for testing.
    print(get_bus_stop_information(""))
    print(get_bus_arrival_predictions(""))

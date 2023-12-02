#!/usr/bin/python
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import requests
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

def get_arrival_predictions(stop_id):
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

def get_stop_information(stop_id):
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

if __name__ == "__main__":
    print(get_stop_information(""))
    print(get_arrival_predictions(""))
#!/usr/bin/python
from dataclasses import dataclass
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
    time_to_arrival: str

def get_arrival_predictions(stop_id):
    logging.info(f"Pulling arrival info for {stop_id}.")
    url = f"https://api.tfl.gov.uk/StopPoint/{stop_id}/Arrivals"

    request = requests.get(url)
    return request.json()

def get_stop_information(stop_id):
    logging.info(f"Pulling stop details for {stop_id}")
    url = f"https://api.tfl.gov.uk/StopPoint/{stop_id}"

    request = requests.get(url)
    data = request.json()

    stop_name = data["commonName"]
    child_stop = find_child_stop(data["children"], stop_id)
    stop_type = child_stop["modes"]
    stop_code = child_stop["stopLetter"]

    return Stop(stop_name, stop_type, stop_code)

def find_child_stop(children, stop_id): # TfL supplies a list of children for specific bus stops, etc. We need to find the correct child from the StopPoint data.
    child_ids = [child["naptanId"] for child in children]
    child_index = child_ids.index(stop_id)
    return children[child_index]

if __name__ == "__main__":
    print(get_stop_information("490006335N"))
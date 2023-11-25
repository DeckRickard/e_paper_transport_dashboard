from dataclasses import dataclass
import logging
from math import floor
from datetime import datetime
import requests
import json

@dataclass
class Weather(object):
    temperature: int
    weather_condition: int

logging.basicConfig(level=logging.DEBUG)

with open("./settings.json") as file:
    settings = json.load(file)["weather"]

def get_raw_weather_data(lat, long): # Returns weather data for a given latitude/longtitude at the current time.
    logging.info("Pulling current weather forecast from API.")
    url = "https://api-metoffice.apiconnect.ibmcloud.com/metoffice/production/v0/forecasts/point/hourly?excludeParameterMetadata=false&includeLocationName=false&latitude={}&longitude={}".format(lat, long)
    
    headers = {
        "X-IBM-Client-Id": settings["metOffice_api_client_id"],
        "X-IBM-Client-Secret": settings["metOffice_api_client_secret"],
        "accept": "application/json"
    }

    request = requests.get(url, headers=headers)
    return request.json()["features"][0]["properties"]["timeSeries"][0] #This is accessing the first in the list of weather forecasts, which should be the most up-to-date.

def write_weather_to_file(filename, value): #Writes the response JSON to a file.
    logging.info("Writing weather data to cache file.")
    file_to_write = open(filename, 'w')
    json.dump(value, file_to_write, indent=6)

def get_current_weather(weather_file):
    with open(weather_file) as file:
        data = json.load(file)

    current_temp = floor(data["screenTemperature"])
    weather_condition = data["significantWeatherCode"]

    return Weather(current_temp, weather_condition)

if __name__ == "__main__":
    #write_weather_to_file('./weather_cache.json', get_raw_weather_data(settings["weather_latitude"], settings["weather_longtitude"]))
    print(get_current_weather("./weather_cache.json"))
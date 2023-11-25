import logging
import datetime
import requests
import json

with open("./settings.json") as file:
    settings = json.load(file)["weather"]

def get_weather(lat, long): # Returns weather data for a given latitude/longtitude.
    url = "https://api-metoffice.apiconnect.ibmcloud.com/metoffice/production/v0/forecasts/point/daily?excludeParameterMetadata=false&includeLocationName=false&latitude={}&longitude={}".format(lat, long)

    headers = {
        "X-IBM-Client-Id": settings["metOffice_api_client_id"],
        "X-IBM-Client-Secret": settings["metOffice_api_client_secret"],
        "accept": "application/json"
    }

    request = requests.get(url, headers=headers)
    return request.json()


print(get_weather(settings["weather_latitude"], settings["weather_longtitude"]))
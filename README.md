# Raspberry Pi E-Paper London Transport Dashboard
![IMG_20231210_160150](https://github.com/r-jeffery-wall/e_paper_transport_dashboard/assets/84279240/4dfcd5f4-9a73-4ad0-b769-39139d198ecc)
## About
This code powers a transport dashboard using the [TfL API](https://api.tfl.gov.uk) and [Real Time Trains API](https://www.realtimetrains.co.uk/about/developer/) for National Rail departures. The information is intended to be drawn to a [5.83" black-and-white E-Paper display](https://www.waveshare.com/product/raspberry-pi/displays/e-paper/5.83inch-e-paper-hat.htm) from Waveshare. The display contains a `settings.json` where four stations/stops can be configured to have departure information pulled from.
There is also a weather display in the corner which uses the [Met Office API](https://www.metoffice.gov.uk/services/data/datapointhttps://www.metoffice.gov.uk/services/data/datapoint). Live departure information is updated every minute, whilst weather information is updated every hour. This is to confirm to the free usage limit of the MetOffice API.

Every effort has been made to make this code widely usable, but users with different hardware may have to modify the code to make the code work.
## Installation
Simply clone the repository to a location on your Raspberry Pi. We will then set up `crontab` to run the code at certain intervals. Your `crontab` should look like this:
![image](https://github.com/r-jeffery-wall/e_paper_transport_dashboard/assets/84279240/bda50a6d-d929-4638-a7ae-816867df121f)
You will need to modify these commands to make sure they point to the folder where your scripts are located.
## Configuration
All configuration is done through the `settings.json` file in the root folder of the repository. An example is provided to illustrate how to use this file. You will need to provide your latitude/longtitude and API credentials for the MetOFfice API, as well as an API credential for the Real Time Trains. You will need to sign up for these services yourself and provide your own API keys to the program. You then will have to define four locations for which to pull departure information.
These require an ID and a type to function. For tube and bus stops, you can use the [TfL API stopPoint search](https://api-portal.tfl.gov.uk/api-details#api=StopPoint&operation=StopPoint_SearchByQueryQueryQueryModesQueryFaresOnlyQueryMaxResultsQueryLine) to find the ID, whilst for national rail train stations you can use the three-letter CRS code which can be found by searching for the station on the [journey planner](https://www.nationalrail.co.uk).

![Screenshot 2023-12-10 162901](https://github.com/r-jeffery-wall/e_paper_transport_dashboard/assets/84279240/cf98dbfd-e930-4010-95a0-26f880c2ee53)

It is recommended to use the provided `example_settings.json` file as a template to configure the program. Just remember to rename this file to `settings.json` when finished.
There are currently three accepted station types:
1. Bus `"bus"`
2. Tube `"tube"`
3. National Rail `"natl_rail"`
The scripts have not been tested with other types of station/stop such as DLR or London Overground, although these may work with the already provided station types. The program also currently cannot deal with locations deemed as 'hubs' by TfL (e.g: Large bus/rail/tube interchanges such as Vauxhall), as the data from these kind of locations is presented in a different format.
## Development
This is a very early version of this project. As I work on it further there are a few key goals I have in mind:
1. Add more accepted stop types.
2. Refactor code to be more efficient and use less API calls.
3. Improve documentation to make it easier for others to use this program.

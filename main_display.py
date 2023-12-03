#!/usr/bin/python
import sys
import os
import logging
from waveshare_epd import epd5in83_V2
from get_date_time import get_date_time_string
import time
import json
from PIL import Image,ImageDraw,ImageFont
from weather_getters import get_formatted_weather_string
from transport_getters import get_bus_arrival_predictions, get_bus_stop_information

#Pictures and fonts will be stored here.
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')

# Global Font definitions
font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
weather_font = ImageFont.truetype(os.path.join(picdir, 'wef_____.ttf'), 46)

logging.basicConfig(level=logging.DEBUG)

def draw_weather():
    formatted_weather = get_formatted_weather_string()
    
    # Drawing weather information
    image = Image.new('1', (98, 96), 255)
    draw = ImageDraw.Draw(image)
    draw.text((49, 0), text=formatted_weather.weather_icon, font=weather_font, anchor="ma")
    draw.text((49, 30), text=formatted_weather.weather_description, font=font14, anchor="ma")
    draw.text((49, 65), text=formatted_weather.temperature, font = font18, anchor="ma")

    return image

def draw_stop_information(stop):
    stop_id = stop["id"]
    stop_type = stop["type"]
    if stop_type == "bus":
        stop = get_bus_stop_information(stop_id)
        arrivals = get_bus_arrival_predictions(stop_id)

        # Drawing stop information
        image = Image.new('1', (322, 190), 255)
        draw = ImageDraw.Draw(image)
        if len(stop.name) > 19: # Stop names that are too long will be shorted with ellipsis.
            draw.text((0, 0), text=''.join(stop.name[:19]) + '...', font=font24)
        else:
            draw.text((0, 0), text=stop.name, font=font24)
        #draw.text((235, 0), text=stop.type, font=font24)
        image.paste(Image.open(os.path.join(picdir, 'icons8-bus-24.png')), (235, 0))
        draw.text((280, 0), text=stop.code, font=font24)
        draw.line((0, 27, 322, 27), fill=0, width=2)

        arrival_y = 29
        for arrival in arrivals:
            draw.text((0, arrival_y), text=arrival.line, font=font18)
            if len(arrival.destination) > 28: # Destination will be shortened if too long.
                draw.text((50, arrival_y), text=''.join(arrival.destination[:28]) + '...', font=font18)
            else:
                draw.text((50, arrival_y), text=arrival.destination, font=font18)
            draw.text((295, arrival_y), text=arrival.formatted_arrival_time, font=font18)
            arrival_y += 20
    
        return image

def main():
    try:
        logging.info("Display refreshing")
        
        # Load settings
        with open("./settings.json") as file:
            settings = json.load(file)["transport"]

        # Display clearing and initialisation done here.
        epd = epd5in83_V2.EPD()
        logging.info("init")
        epd.init()
        time.sleep(1)
        
        # Drawing on the Horizontal image
        logging.info("1.Drawing on the image...") 
        HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 648*480 
        drawblack = ImageDraw.Draw(HBlackimage)

        # Layout variables:
        half_width = int(epd.width / 2)
        banner_height = int(epd.height * 0.2)
        main_height = int(epd.height * 0.8)
        half_main_height = int((main_height / 2) + banner_height)
        weather_x_pos = int(epd.width * 0.85)
        info_1_x = 0
        info_1_y = banner_height + 2
        info_2_x = half_width + 2
        info_2_y = banner_height + 2
        info_3_x = 0
        info_3_y = half_main_height + 2
        info_4_x = half_width + 2
        info_4_y = half_main_height + 2
    
        # Drawing basic layout.
        drawblack.line((0, banner_height, epd.width, banner_height), fill = 0, width = 2)
        drawblack.line((half_width, banner_height, half_width, epd.height), fill = 0, width = 2)  
        drawblack.line((0, half_main_height, epd.width, half_main_height), fill = 0, width = 2)

        # Date and Time banner
        drawblack.text((0, 48), text=get_date_time_string(), font = font32, anchor="lm")
        drawblack.line((weather_x_pos - 2, 0, weather_x_pos - 2, banner_height), fill = 0, width= 2)

        # Weather Info
        HBlackimage.paste(draw_weather(), (weather_x_pos, 0))

        # Transport info
        HBlackimage.paste(draw_stop_information(settings["stop_id_1"]), (info_1_x, info_1_y))
        HBlackimage.paste(draw_stop_information(settings["stop_id_2"]), (info_2_x, info_2_y))       
        HBlackimage.paste(draw_stop_information(settings["stop_id_3"]), (info_3_x, info_3_y))       
        HBlackimage.paste(draw_stop_information(settings["stop_id_4"]), (info_4_x, info_4_y))       

        # Drawn image is saved to a buffer.
        epd.display(epd.getbuffer(HBlackimage))
        time.sleep(2)
        
        # Display goes to sleep.
        logging.info("Goto Sleep...")
        epd.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in83_V2.epdconfig.module_exit()
        exit()

if __name__ == "__main__":
    main()
#!/usr/bin/python
import sys
import os
import logging
from waveshare_epd import epd5in83_V2
from get_date_time import get_date_time_string
import time
from PIL import Image,ImageDraw,ImageFont
from weather_getters import get_current_weather, format_temperature, format_weather

#Pictures and fonts will be stored here.
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
weather = "./weather_cache.json"

# Global Font definitions
font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

logging.basicConfig(level=logging.DEBUG)

def draw_weather(weather_file):
    weather = get_current_weather(weather_file)

    # Drawing weather information
    image = Image.new('1', (162, 80), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text=format_temperature(weather.temperature), font = font18)

    return image

def main():
    try:
        logging.info("Display refreshing")
        
        # Display clearing and initialisation done here.
        epd = epd5in83_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)
        
        # Drawing on the Horizontal image
        logging.info("1.Drawing on the image...") 
        HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 648*480 
        drawblack = ImageDraw.Draw(HBlackimage)

        # Layout variables:
        half_width = epd.width / 2
        banner_height = epd.height * 0.2
        main_height = epd.height * 0.8
        half_main_height = (main_height / 2) + banner_height
        weather_x_pos = int(epd.width * 0.85)
    
        # Drawing basic layout.
        drawblack.line((0, banner_height, epd.width, banner_height), fill = 0, width = 1)
        drawblack.line((half_width, banner_height, half_width, epd.height), fill = 0, width = 1)  
        drawblack.line((0, half_main_height, epd.width, half_main_height), fill = 0, width = 1)

        # Date and Time banner
        drawblack.text((0, 10), text=get_date_time_string(), font = font32)

        # Weather Info
        HBlackimage.paste(draw_weather(weather), (weather_x_pos, 0))
        
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
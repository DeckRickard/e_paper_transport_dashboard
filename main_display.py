#!/usr/bin/python
import sys
import os
import logging
from waveshare_epd import epd5in83_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

#Pictures and fonts will be stored here.
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
print(picdir)

logging.basicConfig(level=logging.DEBUG)

def main():
    try:
        logging.info("Display refreshing")
        
        # Display clearing and initialisation done here.
        epd = epd5in83_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)
        
        # Drawing on the image
        logging.info("Drawing")    
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        
        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...") 
        HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 648*480 
        drawblack = ImageDraw.Draw(HBlackimage)

        # Layout variables:
        half_width = epd.width / 2
        banner_height = epd.height * 0.2
        main_height = epd.height * 0.8
        half_main_height = (main_height / 2) + banner_height
    
        # Drawing basic layout.
        drawblack.line((0, banner_height, epd.width, banner_height), fill = 0, width = 1)
        drawblack.line((half_width, banner_height, half_width, epd.height), fill = 0, width = 1)  
        drawblack.line((0, half_main_height, epd.width, half_main_height), fill = 0, width = 1)


        
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
        epd5in83b_V2.epdconfig.module_exit()
        exit()

if __name__ == "__main__":
    main()
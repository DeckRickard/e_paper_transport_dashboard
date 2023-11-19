#!/usr/bin/python
import sys
import os
import logging
from waveshare_epd import epd5in83b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd5in83b_V2 Demo")
    
    # Display clearing and initialisation done here.
    epd = epd5in83b_V2.EPD()
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
    HRYimage = Image.new('1', (epd.width, epd.height), 255)  # 648*480  HRYimage: red or yellow image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)
    drawblack.text((10, 0), 'hello world', font = font24, fill = 0)
    drawblack.text((10, 20), 'Transport dashboard', font = font24, fill = 0)    
    drawblack.line((20, 50, 70, 100), fill = 0)
    drawblack.line((70, 50, 20, 100), fill = 0)
    drawblack.rectangle((20, 50, 70, 100), outline = 0)    
    drawry.line((165, 50, 165, 100), fill = 0)
    drawry.line((140, 75, 190, 75), fill = 0)
    drawry.arc((140, 50, 190, 100), 0, 360, fill = 0)
    drawry.rectangle((80, 50, 130, 100), fill = 0)
    drawry.chord((200, 50, 250, 100), 0, 360, fill = 0)
    # Drawn image is saved to a buffer.
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    
    # This shows the rationale for displaying images from a file.
    logging.info("3.read bmp file")
    HBlackimage = Image.open(os.path.join(picdir, '5in83b_V2_b.bmp'))
    HRYimage = Image.open(os.path.join(picdir, '5in83b_V2_r.bmp'))
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    
    # Below code is used to clear and sleep the display. This probably won't be neccessary.
    #logging.info("Clear...")
    #epd.init()
    #epd.Clear()
    
    #logging.info("Goto Sleep...")
    #epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83b_V2.epdconfig.module_exit()
    exit()

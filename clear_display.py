#!/usr/bin/python
#Just a quick helper function that can be run as a file by a cronjob to clear the display.
import logging
from waveshare_epd import epd5in83_V2

logging.basicConfig(level=logging.DEBUG)


def clear_display():
    epd = epd5in83_V2.EPD()
    logging.info("Clearing the Display.")
    epd.init()
    epd.Clear()
    epd.sleep()


if __name__ == "__main__":
    clear_display()

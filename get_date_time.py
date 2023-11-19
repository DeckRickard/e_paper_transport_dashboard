#!/usr/bin/python
from datetime import datetime

def get_date_time_string():
    date_time = datetime.now()
    return date_time.strftime("%A %-d %B %Y  %-H:%M")


if __name__ == "__main__":
    print(get_date_time_string())
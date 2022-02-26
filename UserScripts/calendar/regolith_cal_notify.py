#!/usr/bin/env python3

from dotenv import dotenv_values
from icalevents.icalevents import events as ical_events
from datetime import date, datetime
from os import system as shell
from os import path
import subprocess
from time import sleep

def connection():
    try:
        return subprocess.run(
            ['wget', '-q', '--spider', 'google.com'],
            timeout = 3
        ).returncode == 0
    except subprocess.TimeoutExpired:
        return False

def pipe_events():
    dir_path = path.dirname(path.realpath(__file__))
    config = dotenv_values(f'{dir_path}/.env')

    today = date.today()
    yy, mm, dd = today.year, today.month, today.day

    today_start = datetime( yy, mm, dd )
    today_end = datetime( yy, mm, dd+1 )

    try:
        for cal in config:
            cal_events = ical_events(
                url=config[cal],
                start=today_start,
                end=today_end
            )
            
            for evt in cal_events:
                evtstr = str(evt)
                evt_time = evtstr[11:16]
                evt_info = evtstr[27:]
                shell(
                    f'notify-send -a Calendar "{evt_time} {cal.capitalize()}" "{evt_info}"'
                )
        shell(f'echo "{datetime.now()} iCal Notification Success" >>/tmp/regolith_calendar.out')
        
    except:
        shell('echo "{datetime.now()} iCal Notification Fail" >>/tmp/regolith_calendar.out')

if __name__ == "__main__":
    connected = False
    while not connected:
        sleep(15)
        if connection():
            connected = True
            pipe_events()

#!/bin/bash

DISPLAY=:0 nohup python3 /home/pi/alarm_clock/alarm_clock.py >/dev/null 2>&1 &

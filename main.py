#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import datetime
import time
import util

import schedule
from device import device_monitor

def startup():
    now = datetime.datetime.now()
    hour = now.hour
    greeting = None

    if hour <= 7:
        greeting = "早上好，韩大大"
    elif hour <= 12:
        greeting = "上午好，韩大大"
    elif hour <= 18:
        greeting = "下午好，韩大大"
    else:
        greeting = "晚上好，韩大大"

    util.speak(greeting)


if __name__ == "__main__":
    config.load_config()

    print "Init..."
    startup()

    schedule.every(5).seconds.do(device_monitor)

    while True:
        schedule.run_pending()
        time.sleep(1)

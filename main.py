#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys
import time
import schedule

from app import Application
from plugins.builtin import speak


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

    speak(greeting)


if __name__ == "__main__":
    print "Init..."
    startup()

    device = Application('device')
    network = Application('network')

    schedule.every(5).seconds.do(lambda: device.run())
    schedule.every(5).seconds.do(lambda: network.run())

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        speak("Goodbye, master!")
        sys.exit(0)

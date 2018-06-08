#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys
import time
import schedule

from plugins.builtin import speak
from plugins.greeting import hello
from plugins.network import connect
from plugins.device import monitor


if __name__ == "__main__":
    hello()

    schedule.every(5).seconds.do(connect)
    schedule.every(5).seconds.do(monitor)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        speak("Goodbye, master!")
        sys.exit(0)

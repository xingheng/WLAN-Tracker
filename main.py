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
from plugins.solar_terms import solar_term_status, solar_term_alarm


if __name__ == "__main__":
    hello()
    solar_term_status()

    schedule.every(5).seconds.do(connect)
    schedule.every(5).seconds.do(monitor)
    schedule.every(1).minutes.do(solar_term_alarm)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        speak("Goodbye, master!")
        sys.exit(0)

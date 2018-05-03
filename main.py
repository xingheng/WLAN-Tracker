#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import time
import datetime
import schedule

from tabulate import tabulate
from database import *
from ping import *


def main():
    print "Analyzing..."
    db = DB()

    for entity in config.HOSTS:
        alias, hostname = entity.name, entity.hostname
        result, output, error = ping(hostname)
        if result:
            res, ip, mac = arp(hostname)
            last_time = db.get_latest_record(mac)

            if last_time is None or time.time() - last_time > 60.0:
                db.save_record(time.time(), mac, alias, hostname, ip)
                print "Saved %s: %s => %s" % (alias, mac, ip)
            else:
                print alias + " is active just now, time: " + str(last_time)
        else:
            print alias + " is down"

    print "\nTotal device records:\n"
    rows = []

    for record in db.get_all_devices():
        ts = db.get_latest_record(record.mac)
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        rows.append([record.alias, record.mac, date])

    print tabulate(rows, headers=['Name', 'MAC', 'Last Active Time'])

    print "\nDone!\n" + "-" * 60


if __name__ == "__main__":
    config.load_config()
    schedule.every(10).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

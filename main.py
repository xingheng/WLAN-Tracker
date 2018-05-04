#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import time
import datetime
import schedule

from tabulate import tabulate
from database import *
from network import *


def main():
    print "Analyzing..."
    hosts = nmap(config.SETTINGS.host_addresses)

    if hosts is None or len(hosts) <= 0:
        print "Didn't scan out any IP addresses!"
        return

    db = DB()

    local_ips = get_local_ip_addresses()

    for host in hosts:
        if host in local_ips:
            print "Skip the local device address: %s" % host
            continue

        res, ip, mac = get_neighbor_address(host)

        if not res:
            print "Fetch mac address failed for %s" % host
            continue

        entities = filter(lambda x: x.mac.upper() == mac.upper(), config.HOSTS)

        if len(entities) <= 0:
            print "Skip this address: %s" % host
            continue

        entity = entities[0]
        alias = entity.name
        last_time = db.get_latest_record(mac)

        if last_time is None or time.time() - last_time > 60.0:
            db.save_record(time.time(), mac, alias, ip)
            print "Saved %s: %s => %s" % (alias, mac, ip)
        else:
            print alias + " is active just now, time: " + str(last_time)

    print "\nTotal device records:\n"
    rows = []

    for record in db.get_all_devices():
        ts = db.get_latest_record(record.mac)

        if ts is None or ts <= 0:
            continue

        date = datetime.datetime.fromtimestamp(
            ts).strftime('%Y-%m-%d %H:%M:%S')
        rows.append([record.alias, record.mac, date])

    print tabulate(rows, headers=['Name', 'MAC', 'Last Active Time'])

    print "\nDone!\n" + "-" * 60


if __name__ == "__main__":
    config.load_config()
    schedule.every(5).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

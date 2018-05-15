# -*- coding: utf-8 -*-

import datetime
import time
import config
import scanner

from tabulate import tabulate
from database import *

from ..builtin import speak


def monitor():
    host_block = config.HOST_BLOCK
    host_addresses = config.HOST_ADDRESSES

    if not host_block or not host_addresses:
        print "Lack of host block/addresses!"
        return

    print "Analyzing..."
    hosts = scanner.nmap(host_block)

    if not hosts or len(hosts) <= 0:
        print "Didn't scan out any IP addresses!"
        return

    db = DB(config.DBPATH)

    local_ips = scanner.get_local_ip_addresses()
    skip_local_hosts = []
    skip_unstage_hosts = []

    for host in hosts:
        if host in local_ips:
            skip_local_hosts.append(host)
            continue

        res, ip, mac = scanner.get_neighbor_address(host)

        if not res:
            print "Fetch mac address failed for %s" % host
            continue

        entities = filter(lambda x: x.mac.upper() ==
                          mac.upper(), host_addresses)

        if not entities and len(entities) <= 0:
            skip_unstage_hosts.append(host)
            continue

        entity = entities[0]
        alias, nickname = entity.name, entity.nickname
        last_time = db.get_latest_record(mac)
        delta = time.time() - last_time if last_time else float('inf')

        if delta > 60.0:
            db.save_record(time.time(), mac, alias, nickname, ip)
            print "Saved %s: %s => %s" % (alias, mac, ip)

            if delta > 4 * 60 * 60:  # 4 hours
                speak(u"%s上线啦！" % unicode(nickname))
        else:
            print "%s is active just %ld second(s) ago." % (alias, delta)

    if len(skip_local_hosts) > 0:
        print "Skip these local device address: %s" % ', '.join(
            skip_local_hosts)

    if len(skip_unstage_hosts) > 0:
        print "Skip these unstaged device address: %s" % ', '.join(
            skip_unstage_hosts)

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

    print "\nDone! " + str(datetime.datetime.now()) + "\n" + "-" * 60

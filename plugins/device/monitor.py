# -*- coding: utf-8 -*-

import datetime
import time
import config
import scanner

import os
import sqlite3

from database import DB

from ..builtin import get_logger, speak, F, get_data_file, load_tuple_data

logger = get_logger(__file__, F('.'))


def monitor():
    initialize()

    host_block = config.HOST_BLOCK
    host_addresses = config.HOST_ADDRESSES
    logger = get_logger(__package__)

    if not host_block or not host_addresses:
        logger.error("Lack of host block/addresses!")
        return

    logger.info("Analyzing...")
    hosts = scanner.nmap(host_block)

    if not hosts or len(hosts) <= 0:
        logger.error("Didn't scan out any IP addresses!")
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
            logger.error("Fetch mac address failed for %s" % host)
            continue

        entities = filter(lambda x: mac.upper() in x.mac.upper(), host_addresses)

        if not entities and len(entities) <= 0:
            skip_unstage_hosts.append(host)
            continue

        entity = entities[0]
        alias, nickname = entity.name, entity.nickname
        last_time = db.get_latest_record(mac)
        delta = time.time() - last_time if last_time else float('inf')

        if delta > 60.0:
            db.save_record(time.time(), mac, alias, nickname, ip)
            logger.info("Saved %s: %s => %s" % (alias, mac, ip))

            if delta > 4 * 60 * 60:  # 4 hours
                speak(u"%s上线啦！" % unicode(nickname))
        else:
            logger.info("%s is active just %ld second(s) ago." % (alias, delta))

    if len(skip_local_hosts) > 0:
        logger.info("Skip these local device address: %s" % ', '.join(
            skip_local_hosts))

    if len(skip_unstage_hosts) > 0:
        logger.info("Skip these unstaged device address: %s" % ', '.join(
            skip_unstage_hosts))

    results = os.linesep
    results += 'Name\t\tMAC    Last Active Time' + os.linesep

    for record in db.get_all_devices():
        ts = db.get_latest_record(record.mac)

        if ts is None or ts <= 0:
            continue

        date = datetime.datetime.fromtimestamp(
            ts).strftime('%Y-%m-%d %H:%M:%S')
        results += '%s    %s    %s%s' % (record.alias, record.mac, date, os.linesep)

    results += os.linesep
    logger.info(results)


def initialize():
    path = get_data_file("monitor_hosts.cfg", __file__)

    if os.path.exists(path):
        root = load_tuple_data(path)
        config.HOST_BLOCK = root.host_cidr_block
        config.HOST_ADDRESSES = root.host_addresses
    else:
        with open(path, 'w') as f:
            f.write('''
{
    "host_cidr_block": "192.168.31.1/24",
    "host_addresses": [
        {
            "name": "Will's iPhone",
            "mac": "FF:FF:FF:FF:FF:FF",
            "nickname": "My iPhone 6"
        }
    ]
}
            '''.strip())

        logger.info('Initialized a configuration file at %s', path)

    path = get_data_file("device.sqlite", __file__)
    config.DBPATH = path

    if not os.path.exists(path):
        try:
            with sqlite3.connect(path) as conn:
                conn.execute('''CREATE TABLE `device` (
                    `mac`	TEXT NOT NULL,
                    `alias`	TEXT,
                    `nickname`	TEXT,
                    `ip`	TEXT,
                    `timestamp`	REAL,
                    PRIMARY KEY(mac)
                );''')
                conn.commit()

            logger.info('Initialized a database file at %s', path)
        except Exception as e:
            logger.error(e)

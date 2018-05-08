#!/usr/bin/env python

import os
import sqlite3


def create_db():
    cur_dir = os.path.dirname(__file__)
    path = os.path.join(cur_dir, "data/main.sqlite")

    if os.path.exists(path):
        print "database exists: %s" % path
        return False

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

        return True
    except Exception as e:
        print(e)

    return False


def create_default_config():
    cur_dir = os.path.dirname(__file__)
    path = os.path.join(cur_dir, "data/configure.json")

    if os.path.exists(path):
        print "host config file exists: %s" % path
        return False

    with open(path, 'w') as f:
        f.write('''
{
    "hosts": [
        {
            "name": "Will's iPhone",
            "mac": "XX:XX:XX:XX:XX:XX",
            "nickname": "A gift from Steve"
        }
    ],
    "settings": {
        "host_addresses": "192.168.1.1/24"
    },
    "keys": {
        "baidu_tts_appid": "xxxx",
        "baidu_tts_appkey": "xxxx",
        "baidu_tts_secret": "xxxx"
    }
}
        ''')

    return True


if __name__ == "__main__":
    cur_dir = os.path.dirname(__file__)
    path = os.path.join(cur_dir, "data")
    if not os.path.exists(path):
        os.mkdir(path)

    if create_db():
        print "Created a database including tables successfully."

    if create_default_config():
        print "Created a host config file successfully."

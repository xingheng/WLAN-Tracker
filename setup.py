#!/usr/bin/env python

import os
import sqlite3


def create_db():
    path = os.path.abspath("./data/main.sqlite")

    if os.path.exists(path):
        print "database exists: %s" % path
        return False

    try:
        with sqlite3.connect(path) as conn:
            conn.execute('''CREATE TABLE `record` (
                            `timestamp`	REAL NOT NULL,
                            `mac`	TEXT NOT NULL,
                            `alias`	TEXT,
                            `hostname`	TEXT,
                            `ip`	TEXT,
                            PRIMARY KEY(timestamp, mac)
                        );''')
            conn.commit()

        return True
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return False


def create_default_host_config():
    path = os.path.abspath("./data/hosts.json")

    if os.path.exists(path):
        print "host config file exists: %s" % path
        return False

    with open(path, 'w') as f:
        f.write('''
{
    "hosts": [
        {
            "name": "Will's iPhone",
            "hostname": "Wills-iPhone.local"
        }
    ]
}
        ''')

    return True


if __name__ == "__main__":
    if create_db():
        print "Created a database including tables successfully."

    if create_default_host_config():
        print "Created a host config file successfully."

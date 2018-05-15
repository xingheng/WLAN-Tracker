import os
import sqlite3
import config
from monitor import monitor


def setup(app):
    app.register_formatter(monitor)
    path = app.get_sandbox_file("monitor_hosts.cfg")

    if os.path.exists(path):
        root = app.load_tuple_data(path)
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

        print('Initialized a configuration file at %s' % path)

    path = app.get_sandbox_file("device.sqlite")
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

            print('Initialized a database file at %s' % path)
        except Exception as e:
            print(str(e))

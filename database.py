
import os
import sqlite3
from collections import namedtuple


def namedtuple_factory(cursor, row):
    # http://peter-hoffmann.com/2010/python-sqlite-namedtuple-factory.html
    """
    Usage:
    con.row_factory = namedtuple_factory
    """
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


class DB:
    def __init__(self):
        cur_dir = os.path.dirname(__file__)
        self.conn = sqlite3.connect(os.path.join(cur_dir, 'data/main.sqlite'))
        self.conn.row_factory = namedtuple_factory

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def save_record(self, timestamp, mac, alias, ip):
        c = self.conn.cursor()

        c.execute('INSERT OR REPLACE INTO record (timestamp, mac, alias, ip) VALUES (?,?,?,?)',
                  (timestamp, mac.upper(), alias, ip))

        self.conn.commit()

    def get_all_devices(self):
        c=self.conn.cursor()
        c.execute("SELECT DISTINCT(mac), alias FROM record;")
        return c.fetchall()

    def get_latest_record(self, mac):
        c=self.conn.cursor()
        c.execute(
            "SELECT timestamp FROM record WHERE mac == '%s' ORDER BY timestamp DESC LIMIT 1;" % mac.upper())
        result = c.fetchone()
        return result.timestamp if result else None


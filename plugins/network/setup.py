import os
from ping import *

HOSTNAME = None


def connect():
    if not HOSTNAME:
        print "Lack of hostname for connection."
        return

    res, output, error = ping(HOSTNAME)

    print output


def setup(app):
    app.register_formatter(connect)
    path = app.get_sandbox_file("connection.cfg")

    if os.path.exists(path):
        root = app.load_tuple_data(path)
        global HOSTNAME
        HOSTNAME = root.connectivity
        return

    with open(path, 'w') as f:
        f.write('''
{
    "connectivity": "192.168.31.1"
}
        '''.strip())

    print 'Initialized a configuration file at %s' % path

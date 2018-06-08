import os
from ping import *

from ..builtin import get_logger, F, get_data_file, load_tuple_data

logger = get_logger(__file__, F('.'))

HOSTNAME = None


def connect():
    initialize()

    if not HOSTNAME:
        logger.error("Lack of hostname for connection.")
        return

    res, output, error = ping(HOSTNAME)

    logger.info('Host %s is %s!', HOSTNAME, 'available' if res else 'offline')

    if not res:
        logger.info(output)
        logger.error(error)


def initialize():
    path = get_data_file("connection.cfg", __file__)

    if os.path.exists(path):
        root = load_tuple_data(path)
        global HOSTNAME
        HOSTNAME = root.connectivity
        return

    with open(path, 'w') as f:
        f.write('''
{
    "connectivity": "192.168.31.1"
}
        '''.strip())

    logger.info('Initialized a configuration file at %s', path)

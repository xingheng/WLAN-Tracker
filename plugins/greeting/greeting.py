# -*- coding: utf-8 -*-

import os
import datetime

from ..builtin import get_logger, speak, F, get_data_file, load_tuple_data

logger = get_logger(__file__, F('.'))
NAME = None


def hello():
    now = datetime.datetime.now()
    hour = now.hour
    greeting = None

    if hour <= 7:
        greeting = u"早上好！"
    elif hour <= 12:
        greeting = u"上午好！"
    elif hour <= 18:
        greeting = u"下午好！"
    else:
        greeting = u"晚上好！"

    if not NAME:
        initialize()

    speak(greeting + unicode(NAME if NAME else ''))


def initialize():
    path = get_data_file("greeting.cfg", __file__)

    if os.path.exists(path):
        root = load_tuple_data(path)
        global NAME
        NAME = root.master_name
        return True

    with open(path, 'w') as f:
        f.write('''
{
    "master_name": "Master"
}
        '''.strip())

    logger.info('Initialized a configuration file at %s', path)
    return False


if __name__ == "__main__":
    hello()

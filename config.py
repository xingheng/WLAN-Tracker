#!/usr/bin/env python

import json
from collections import namedtuple

HOSTS = None
SETTINGS = None

def load_config():
    '''
    Inspired from https://stackoverflow.com/a/15882054/1677041
    '''

    with open("./data/hosts.json") as f:
        root = json.loads(f.read(), object_hook=lambda d: namedtuple('HostEntity', d.keys())(*d.values()))

        global HOSTS, SETTINGS
        HOSTS = root.hosts
        SETTINGS = root.settings

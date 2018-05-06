
import os
import json
from collections import namedtuple

HOSTS = None
SETTINGS = None
KEYS = None

def load_config():
    '''
    Inspired from https://stackoverflow.com/a/15882054/1677041
    '''

    cur_dir = os.path.dirname(__file__)
    with open(os.path.join(cur_dir, "data/hosts.json")) as f:
        root = json.loads(f.read(), object_hook=lambda d: namedtuple('HostEntity', d.keys())(*d.values()))

        global HOSTS, SETTINGS, KEYS
        HOSTS = root.hosts
        SETTINGS = root.settings
        KEYS = root.keys

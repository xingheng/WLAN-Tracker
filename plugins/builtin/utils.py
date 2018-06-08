# -*- coding: utf-8 -*-
'''
Invoke the baidu text-to-speech to synthesis voice.
'''

import os
import json
from collections import namedtuple
from logger import get_logger
from os.path import abspath as F


def get_data_file(filename, module_path):
    return os.path.join(os.path.dirname(module_path), 'data', filename)


def load_tuple_data(filepath, typename = 'Entity'):
    '''
    Inspired from https://stackoverflow.com/a/15882054/1677041
    '''
    with open(filepath) as f:
        return json.loads(f.read(), object_hook=lambda d: namedtuple(
            typename, d.keys())(*d.values()))

    return None

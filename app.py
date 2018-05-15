#!/usr/bin/env python
'''
Plugin application.
'''

import os
import json
from collections import namedtuple
from functools import partial
from pluginbase import PluginBase


# For easier usage calculate the path relative to here.
here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)


class Application(object):

    def __init__(self, name):
        self.name = name
        self.formatter = None

        builtin_path = get_path('plugins/builtin')
        plugin_base = PluginBase(package='app.plugins',
                                 searchpath=[builtin_path])

        builtin_source = plugin_base.make_plugin_source(
            searchpath=[builtin_path])

        for plugin_name in builtin_source.list_plugins():
            plugin = builtin_source.load_plugin(plugin_name)
            plugin.setup(self)

        self.source = plugin_base.make_plugin_source(
            searchpath=[get_path('./plugins')],
            identifier=self.name)

        try:
            plugin = self.source.load_plugin(self.name)
            plugin.setup(self)
        except AttributeError as e:
            print e

    def register_formatter(self, formatter):
        self.formatter = formatter

    def run(self):
        if self.formatter:
            try:
                self.formatter()
            except Exception as ex:
                print ex
        else:
            print '%s app could be run without formatter!' % self.name

    def get_generic_file(self, name):
        generic_path = get_path('data/generic')

        if not os.path.exists(generic_path):
            os.mkdir(generic_path)

        return get_path('%s/%s' % (generic_path, name))

    def get_sandbox_file(self, name):
        sandbox_path = get_path('data/%s' % self.name)

        if not os.path.exists(sandbox_path):
            os.mkdir(sandbox_path)

        return get_path('%s/%s' % (sandbox_path, name))

    def load_tuple_data(self, filepath):
        with open(filepath) as f:
            # Inspired from https://stackoverflow.com/a/15882054/1677041
            return json.loads(f.read(), object_hook=lambda d: namedtuple(
                'ConfigEntity', d.keys())(*d.values()))

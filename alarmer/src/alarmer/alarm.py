#!/usr/bin/env python
#coding:utf-8

import types
import sys
import getopt
import subprocess, shlex
import time
import re
import datetime

__all__ = ['Checker', 'Informer', 'Main']


class Informer(object):

    def __init__(self, main, **kwargs):
        self._options = main.options(kwargs)

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass

    def alarm(self, **kwargs):
        return True, None


class Checker(object):
    _informers = []

    def __init__(self, main, **kwargs):
        self._options = main.options(kwargs)
        main._checkers.append(self)

    def __setattr__(self, key, val):
        if key.startswith('_') or hasattr(self, key):
            return super(Checker, self).__setattr__(key, val)
        if key == 'informers':
            self._informers += val
        else:
            self._options[key] = val

    def __getattr__(self, key):
        if key.startswith('_') or hasattr(self, key):
            return super(Checker, self).__getattr__(key)
        if key == 'informers':
            self._informers[key]
        else:
            self._options[key]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get(self):
        return 0

    def check(self):
        value = self.get()
        return True, None


class Main(object):
    _checkers = []
    _default_plugins = [Checker, Informer]
    _options = {
        "name": "Alarm",
        "message": "[$datetime] Alarm $name",
        "sleep": 1
    }

    def __init__(self, **kwargs):
        self._options.update(kwargs)
        self.inject(self._options.get("plugins", []))

    def _plugin(self, plugin):
        def __plugin(self, **kwargs):
            return plugin(self, **kwargs)
        return types.MethodType(__plugin, self)

    def inject(self, plugins):
        for plugin in plugins + self._default_plugins:
            setattr(self, plugin.__name__, self._plugin(plugin))


    def run(self):
        while True:
            for checker in self._checkers:
                res, value = checker.check()

                if not res:
                    for informer in checker._informers:
                        informer.alarm(value=value)

            time.sleep(self._options["sleep"])


    def options(self, opts):
        ret = self._options.copy()
        ret.update(opts)
        ret.update({"datetime": datetime.datetime.now()})
        return ret
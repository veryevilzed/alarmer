#!/usr/bin/env python
#coding:utf-8

import types
import sys
import getopt
import subprocess, shlex
import time
import re
import datetime

from checkers.sysinfo import Ram, CPU, Disk, Ping 
from informers.console import Console
from informers.curl import Curl
from informers.mail import Email
from informers.hipchat import HipChat

__all__ = ['Main']


class Options(dict):
    def merge(self, *args):
        ret = Options(self)
        for a in args:
            ret.update(a)
        return ret


class Main(object):
    _checkers = []
    _default_plugins = [Ram, CPU, Disk, Ping, Console, Curl, Email, HipChat]
    _options = {
        "name": "Alarm",
        "message": "[$datetime] Alarm $name",
        "sleep": 1
    }

    def __init__(self, **kwargs):
        self.opts = Options().merge(self._options, kwargs)
        self.inject(self.opts.get("plugins", []))

    def plugin(self, plugin):
        def _plugin(self, **kwargs):
            return plugin(self, **kwargs)
        return types.MethodType(_plugin, self)

    def inject(self, plugins):
        for plugin in plugins + self._default_plugins:
            setattr(self, plugin.__name__, self.plugin(plugin))

    def run(self):
        while True:
            for checker in self._checkers:
                res, value = checker.check()

                if not res:
                    for informer in checker.opts.get("informers", []):
                        informer.alarm(value=value, checker=checker)

            time.sleep(self.opts["sleep"])

    def options(self, *opts):
        ret = self.opts.merge(*opts)
        ret.update({"datetime": datetime.datetime.now()})
        return ret

#coding:utf-8

import psutil, os, re
from plumbum import local
from base import Checker


class Ram(Checker):
    _options = {
        "name": "RAM free",
        "validate": lambda x: x["value"] < 80
    }

    def update(self):
        value = psutil.virtual_memory().percent
        super(self.__class__, self).update(value)


class CPU(Checker):
    _options = {
        "name": "CPU load",
        "validate": lambda x: x["value"] < 80
    }

    def update(self):
        value = psutil.cpu_percent()
        super(self.__class__, self).update(value)


class Disk(Checker):
    _options = {
        "name": "Disk free",
        "validate": lambda x: x["value"] > 20
    }

    def update(self):
        p = os.statvfs(self._options.get("target", "/") )
        value = p.f_bfree / float(p.f_blocks)
        



class Ping(Checker):
    re = re.compile(r"(\d+\.\d+)% packet loss")
    ping = local['ping']['-c5']
    _options = {
        "name": "PING",
        "validate": lambda x: x["value"] < 21,
        "target": "127.0.0.1",
        "timeout": 2
    }

    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)
        self.opts["name"] = "PING %s" % self.opts.get("target")

    def update(self):
        value = 100.0

        try:
            text = self.ping(self.opts["target"], timeout=self.opts["timeout"])
            m = self.re.search(text)
            if m:
                value = float(m.group(1))
        except:
            pass

        super(self.__class__, self).update(value)

#coding:utf-8

import psutils, os, re
from plumbum import local
from .alarm import Checker


class Ram(Checker):
    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)

    

    def check(self):
        self.update()
        return self.validate

    def update(self):
        self.value = psutil.virtual_memory().percent


class CPU(Checker):
    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)

    def update(self):
        self.value = psutil.cpu_percent()
        return self.value


class Disk(Checker):
    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)
        
    def update(self):
        p = os.statvfs(self._options.get("target", "/") )
        self.value = p.f_bfree / float(p.f_blocks)



class Ping(Checker):
    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)
        self.re = re.compile(r"(\d+\.\d+)% packet loss")
        self.ping = local['ping']['-c1']

    def update(self):
        try:
            text = self.ping(self._options.get("target", timeout=self._options.get("timeout", 2)))
            m = self.re.search(text)
            if not m:
                self.value = 100.0
            self.value = float(m.group(1))
        except:
            self.value = 100.0

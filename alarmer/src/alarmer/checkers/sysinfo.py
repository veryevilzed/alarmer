#coding:utf-8

import psutils, os, re
from plumbum import local


class Ram:
    def __init__(self):
        pass

    

    def check(self):
        self.update()
        return self.validate

    def update(self):
        self.value = psutil.virtual_memory().percent


class CPU:
    def __init__(self):
        pass

    def update(self):
        self.value = psutil.cpu_percent()
        return self.value


class Disk:
    def __init__(self):
        pass
        
    def update(self):
        p = os.statvfs(self._options.get("target", "/") )
        self.value = p.f_bfree / float(p.f_blocks)



class Ping:
    def __init__(self):
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

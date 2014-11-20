#coding:utf-8

import requests
from string import Template
from base import Informer


class Curl(Informer):
    _options = {
        "urls":     [],
        "method":   "GET",
        "body":     "",
        "headers":  [],
        "auth":     None,
        "params":   None,
        "timeout":  5,
        "allow_redirects": True,
        "retry_count": 5,
        "error_count": 1,
    }

    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)

        if type(self.opts["urls"]) in ("str", "unicode"):
            self.opts["urls"] = [self.opts["urls"]]

        self.urls = map(lambda url: Template(url), self.opts["urls"])

    def alarm(self, **kwargs):
        if not super(self.__class__, self).alarm(**kwargs):
            return False

        ok = []
        for url in self.urls:
            req_kwargs = {
                "method": self.opts["method"],
                "url": url.safe_substitute(self.opts), 
                "auth": self.opts["auth"], 
                "allow_redirects": self.opts["allow_redirects"], 
                "timeout": self.opts["timeout"]
            }
            if self.opts["method"] == "GET":
                req_kwargs["params"] = self.opts["params"]
            elif self.opts["method"] == "POST":
                req_kwargs["data"] = self.opts["body"].safe_substitute(self.opts)

            uok = False
            for i in xrange(self.opts["retry_count"]):
                r = requests.request(**req_kwargs)
                r.headers = self.opts["headers"]
                if r.status_code < 300:
                    uok = True
                    break
            ok.append(uok)

        return all(ok)

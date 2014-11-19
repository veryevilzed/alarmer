#coding:utf-8

import requests
from string import Template
from base import Informer


class Curl(Informer):
    _options = {
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
        self._options.update(kwargs)
        super(self.__class__, self).__init__(main, **self._options)

        if type(urls) in ("str", "unicode"):
            self.urls = [self.urls]

        self.urls = map(self.urls, lambda url: Template(url))        


    def _get(self, url, kwargs, params={}):
        r = requests.get(url.safe_substitute(kwargs), params=params, auth=self.auth, allow_redirects=self.allow_redirects, timeout=self.timeout)
        r.headers = self.headers
        if r.status_code < 300:
            return True
        return False


    def _post(self, url, kwargs, params={}):
        r = requests.post(url.safe_substitute(kwargs), data=self.body.safe_substitute(kwargs), auth=self.auth, allow_redirects=self.allow_redirects, timeout=self.timeout)
        r.headers = self.headers
        if r.status_code < 300:
            return True
        return False


    def alarm(self, **kwargs):
        if not super(self.__class__, self).alarm(**kwargs):
            return False

        kwargs = main.options(kwargs)
        params = {}
        if self.params:
            for name in self.params:
                params = kwargs.get(name)

        for url in self.urls:
            for i in xrange(self.retry_count):
                if self.method == "GET":
                    if self._get(url, kwargs, params):
                        break

                if self.method == "POST":
                    if self._post(url, kwargs, params):
                        break

        return True






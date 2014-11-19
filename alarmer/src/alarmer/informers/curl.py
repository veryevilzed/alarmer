#coding:utf-8

import request
from string import Template


class Curl:

    urls = []
    self.method = 'GET'

    def __init__(self, main, **kwargs):
        self.opts            = main.options(kwargs)
        urls = self.opts.get("url", [])
        if type(urls) in ("str", "unicode"):
            self.urls = [urls]

        for url in urls:
            self.urls += [Template(url)]

        self.method          = self.opts.get("method", "GET")
        self.body            = self.opts.get("body",   "")
        self.headers         = self.opts.get("headers",  [])
        self.auth            = self.opts.get("auth",  None)
        self.params          = self.opts.get("params", None)
        self.timeout         = self.opts.get("timeout", 5)
        self.allow_redirects = self.opts.get("allow_redirects", True)
        self.retry_count     = self.opts.get("retry_count", 5)

        self.error_count     = self.opts.get("error_count", 1)
        self._error = 0
        


    def __get(self, url, kwargs, params={}):
        r = requests.get(url.safe_substitute(kwargs), params=params, auth=self.auth, allow_redirects=self.allow_redirects, timeout=self.timeout)
        r.headers = self.headers
        if r.status_code < 300:
            return True
        return False


    def __post(self, url, kwargs, params={}):
        r = requests.post(url.safe_substitute(kwargs), data=self.body.safe_substitute(kwargs), auth=self.auth, allow_redirects=self.allow_redirects, timeout=self.timeout)
        r.headers = self.headers
        if r.status_code < 300:
            return True
        return False


    def alarm(self, **kwargs):

        self._error += 1
        if (self._error < self.error_count):
            return

        self._error = 0

        if (datetime.datetime.now() - self._last_send).total_seconds() < self.delay:
            return 
        self._last_send = datetime.datetime.now()

        kwargs = main.options(kwargs)
        params = {}
        if self.params:
            for name in self.params:
                params = kwargs.get(name)

        for url in self.urls:
            for i in xrange(self.retry_count):
                if self.method == "GET":
                    if self.__get(url, kwargs, params):
                        break

                if self.method == "POST":
                    if self.__get(url, kwargs, params):
                        break







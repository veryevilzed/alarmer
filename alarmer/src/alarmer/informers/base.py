import datetime

class Informer(object):
    _options = {}
    _last_send = datetime.datetime(1980, 2, 1)
    _error = 0

    def __init__(self, main, **kwargs):
        self.opts = main.options(self._options, kwargs)

    def alarm(self, **kwargs):
        self.opts.update(kwargs)

        self._error += 1
        if (self._error < self.opts["error_count"]):
            return False

        self._error = 0
        if (datetime.datetime.now() - self._last_send).total_seconds() < self.opts["delay"]:
            return False

        self._last_send = datetime.datetime.now()
        return True

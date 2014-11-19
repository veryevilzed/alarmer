import datetime

class Informer(object):
    _last_send = datetime.datetime(1980, 2, 1)
    _error = 0

    def __init__(self, main, **kwargs):
        self._options = main.options(kwargs)

    def __setattr__(self, key, val):
        if key.startswith('_') or hasattr(self, key):
            return super(Informer, self).__setattr__(key, val)
        self._options[key] = val

    def __getattr__(self, key):
        if key.startswith('_'):
            return super(Informer, self).__getattr__(key)
        return self._options[key]

    def alarm(self, **kwargs):
        self._error += 1
        if (self._error < self.error_count):
            return False

        self._error = 0
        if (datetime.datetime.now() - self._last_send).total_seconds() < self.delay:
            return False

        self._last_send = datetime.datetime.now()
        return True

import datetime

class Checker(object):
    def __init__(self, main, **kwargs):
        self._options = main.options(kwargs)
        main._checkers.append(self)

    def __setattr__(self, key, val):
        if key.startswith('_') or hasattr(self, key):
            return super(Checker, self).__setattr__(key, val)
        self._options[key] = val

    def __getattr__(self, key):
        if key.startswith('_'):
            return super(Checker, self).__getattr__(key)
        return self._options[key]

    def update(self):
        raise NotImplemented()

    def check(self):
        self.update()
        return self.validate(self), self.value

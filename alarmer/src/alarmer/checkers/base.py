import datetime

class Checker(object):
    _options = {}

    def __init__(self, main, **kwargs):
        self.opts = main.options(self._options, kwargs)
        main._checkers.append(self)

    def update(self, value):
        self.opts["value"] = value
        return value

    def check(self):
        self.update()
        return self.opts["validate"](self.opts), self.opts["value"]

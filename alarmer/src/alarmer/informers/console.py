#cosding:utf-8

import hipchat
import datetime
from string import Template
from base import Informer


class Console(Informer):
    _options = {
        "msg_from": "Alarmer",
        "error_count": 1,
        "delay": 60 * 10,
        "message": "Alarm!"
    }

    def __init__(self, main, **kwargs):
        self._options.update(kwargs)
        super(self.__class__, self).__init__(main, **self._options)
        self.msg = Template(self.message)

    def alarm(self, **kwargs):
        if not super(self.__class__, self).alarm(**kwargs):
            return False

        print self.msg_from, 'wrote', self.msg.safe_substitute(kwargs)
        return True


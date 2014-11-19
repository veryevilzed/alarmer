#cosding:utf-8

import hipchat
import datetime
from base import Informer


class HipChat(Informer):
    _options = {
        "room_id": "",
        "token": "",
        "msg_from": "Alarmer",
        "color": "red",
        "error_count": 1,
        "delay": 60 * 10,
        "message": "Alarm!"
    }

    def __init__(self, main, **kwargs):
        self._options.update(kwargs)
        super(self.__class__, self).__init__(main, **self._options)
        self.hipster = hipchat.HipChat(token=self.token)
        self.msg = Template(self.message)

    def alarm(self, **kwargs):
        if not super(self.__class__, self).alarm(**kwargs):
            return False

        self.hipster.message_room(
            self.room_id, 
            self.msg_from, 
            self.msg.safe_substitute(kwargs), 
            color=self.color)

        return True


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
        "retry_count": 5,
        "delay": 60 * 10,
        "message": "Alarm!"
    }

    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)
        self.hipster = hipchat.HipChat(token=self.token)
        self.msg = Template(self.message)

    def alarm(self, **kwargs):
        if not super(self.__class__, self).alarm(**kwargs):
            return False

        ok = False
        for i in xrange(self.opts["retry_count"]):
            try:
                self.hipster.message_room(
                    self.opts["room_id"], 
                    self.opts["msg_from"], 
                    self.msg.safe_substitute(self.opts), 
                    color=self.opts["color"])
                ok = True
                break
            except:
                pass

        return ok


#cosding:utf-8

import hipchat
import datetime


class HipChat:

    token = ''

    def __init__(self, main, **kwargs):
        self.opts        = main.options(kwargs)
        self.token       = self.opts["token"]
        self.room_id     = self.opts["room_id"]
        self.msg         = Template(self.opts["message"])
        self.name        = self.opts.get("name", "Alarmer")
        self.color       = self.opts.get("color","red")
        self.error_count = self.opts.get("error_count", -1)
        self._error      = 0
        self.hipster     = hipchat.HipChat(token=self.token)
        self.delay       = self.opts.get("delay", 60 * 10)
        self._last_send  = datetime.datetime(1980, 02, 01)

    def alarm(self, **kwargs):
        self._error += 1
        if (self._error < self.error_count):
            return

        self._error = 0

        if (datetime.datetime.now() - self._last_send).total_seconds() < self.delay:
            return 

        kwargs = main.options(kwargs)
        self._last_send = datetime.datetime.now()

        if self.error >= self.error_count or self.error_count == -1:
            self.error = 0
            self.hipster.message_room(
                self.room_id, 
                self.name, 
                self.msg_tmpl.safe_substitute(kwargs), 
                color=self.color)



#cosding:utf-8

import hipchat
import datetime


class Hipster:
    def __init__(self, config):
        self.room_id = config["room_id"]
        self.color = config.get("color","red")
        self.error_message = config.get("message", "Alarm")
        self.apikey = config["apikey"] 
        self.name = config.get("name", "Alarmer")
        self.error_count = int(config.get("error_count", "-1"))
        self.error = 0
        self.hipster = hipchat.HipChat(token=self.apikey)

    def alarm(self, value=""):
        self.error += 1
        if self.error >= self.error_count or self.error_count == -1:
            self.error = 0
            msg = self.error_message % {
                "date": datetime.datetime.now(), 
                "result": value, 
                "small_result": value[:30]
            }
            self.hipster.message_room(
                self.room_id, 
                self.name, 
                msg, 
                color=self.color)



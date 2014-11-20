#coding:utf-8

import smtplib
from string import Template
import datetime
from base import Informer

from email import MIMEText

class Email(Informer):
    _options = {
        "host":         "localhost",
        "username":     None,
        "password":     None,
        "tls":          False,
        "delay":        60 * 10,
        "msg_from":     "",
        "msg_to":       [],
        "error_count":  1,
        "subject":      "[$datetime] Alarm $name",
        "message":      "Alarm!"
    }

    def __init__(self, main, **kwargs):
        super(self.__class__, self).__init__(main, **kwargs)

        self.msg_tmpl_subj = Template(self.subject)
        self.msg_tmpl      = Template(self.message)

        if type(self.opts["msg_to"]) in ("str", "unicode"):
            self.opts["msg_to"] = [self.opts["msg_to"]]

    def _connect(self):
        self.server = smtplib.SMTP(self.opts["host"])
        if self.opts["tls"]:
            self.server.starttls()
        if self.opts["username"]:
            self.server.login(self.opts["username"], self.opts["password"])

    def _close(self):
        self.server.close()

    def alarm(self, *args, **kwargs):
        if not super(self.__class__, self).alarm(**kwargs):
            return False

        self._connect()       
        for msg_to in self.self.opts["msg_to"]:
            msg = MIMEText(self.msg_tmpl.safe_substitute(kwargs))
            msg['Subject'] = self.msg_tmpl_subj.safe_substitute(self.opts)
            msg['From'] = self.opts["msg_from"]
            msg['To'] = msg_to
            self.server.sendmail(self.opts["msg_from"], [msg_to], msg.as_string())
        self._close()

        return True
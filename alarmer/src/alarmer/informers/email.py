#coding:utf-8

import smtplib
from string import Template
import datetime
from base import Informer

#from email import MIMEText

class Email(Informer):
    _options = {
        "host":     "localhost",
        "username": None,
        "password": None,
        "tls":      False,
        "delay":    60 * 10,
        "msg_from":     "",
        "msg_to":       [],
        "error_count": 1,
        "subject":  "[$datetime] Alarm $name",
        "message":  "Alarm!"
    }

    def __init__(self, main, **kwargs):
        self._options.update(kwargs)
        super(self.__class__, self).__init__(main, **self._options)

        self.msg_tmpl_subj = Template(self.subject)
        self.msg_tmpl      = Template(self.message)

        if type(self.to) in ("str", "unicode"):
            self.to = [self.to]

    def _connect(self):
        self.server = smtplib.SMTP(self.host)
        if self.tls:
            self.server.starttls()
        if self.username:
            self.server.login(self.username, self.password)

    def _close(self):
        self.server.close()

    def alarm(self, *args, **kwargs):
        if not super(self.__class__, self).alarm(**kwargs):
            return False

        self._connect()       
        kwargs.update(main.options(kwargs))
        for msg_to in self.msg_to:
            #msg = MIMEText(self.msg_tmpl.safe_substitute(kwargs))
            msg['Subject'] = self.msg_tmpl_subj.safe_substitute(kwargs)
            msg['From'] = self.msg_from
            msg['To'] = msg_to
            self.server.sendmail(self.msg_from, [msg_to], msg.as_string())
        self._close()
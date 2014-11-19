#coding:utf-8

import smtplib
from string import Template
import datetime

from email.mime.text import MIMEText

class Email:

    tls = False
    unsename = ''
    password = ''

    def __init__(self, main, **kwargs):

        self.opts = main.options(kwargs)

        self.error_message = self.opts["message"]
        self.name          = self.opts["name"]
        self.msg_tmpl_subj = Template(self.opts.get("subject", "[$datetime] Alarm $name"))
        self.msg_tmpl      = Template(self.error_message)
        self.msg_from      = self.opts.get("from", None)
        self.msg_to        = self.opts.get("to", [])
        self.host          = self.opts.get("host", 'localhost')

        self.username      = self.opts.get("username", None)
        self.password      = self.opts.get("password", None)
        self.tls           = self.opts.get("tls",     False)

        self.error_count   = self.opts.get("error_count", 1)
        self._error = 0

        self.delay         = self.opts.get("delay", 60 * 10)
        self._last_send    = datetime.datetime(1980, 02, 01)

        if type(self.msg_to) in ("str", "unicode"):
            self.msg_to = [self.msg_to]


    def __connect(self):
        self.server = smtplib.SMTP(self.host)
        if self.tls:
            self.server.starttls()
        if (self.username)
            self.server.login(self.username, self.password)

    def __close(self):
        self.server.close()

    def alarm(self, *args, **kwargs):

        self._error += 1
        if (self._error < self.error_count):
            return

        self._error = 0

        if (datetime.datetime.now() - self._last_send).total_seconds() < self.delay:
            return 


        kwargs = main.options(kwargs)
        self._last_send = datetime.datetime.now()

        self.__connect()       
        kwargs.update(main.options(kwargs))
        for msg_to in self.msg_to:
            msg = MIMEText(self.msg_tmpl.safe_substitute(kwargs))
            msg['Subject'] = self.msg_tmpl_subj.safe_substitute(kwargs)
            msg['From'] = self.msg_from
            msg['To'] = msg_to
            self.server.sendmail(self.msg_from, [msg_to], msg.as_string())
        self.__close()
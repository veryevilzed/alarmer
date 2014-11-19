#coding:utf-8

import smtplib

from email.mime.text import MIMEText

class Email:
    def __init__(self, config):
        self.error_message = config.get("message", "Alarm")
        self.apikey = config["apikey"] 
        self.msg_from = config.get("from", "alarmer@google.com")
        self.msg_to = config.get("to", "").split(" ")

    def alarm(self, value=""):
        s = smtplib.SMTP('localhost')
        
        for msg_to in self.msg_to:
            msg = MIMEText(fp.read())
            msg['Subject'] = 'Alarm'
            msg['From'] = self.msg_from
            msg['To'] = msg_to
            s.sendmail(self.msg_from, [msg_to], msg.as_string())
        s.close()
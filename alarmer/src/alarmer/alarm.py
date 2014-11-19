#!/usr/bin/env python
#coding:utf-8

import sys
import getopt
import configparser
import subprocess, shlex
import time
import re
import hipchat
import datetime
import plugins.hipster

class Alarmer:

    def shell_check(self):
        if not self.shell:
            return None
        try:
            result = subprocess.check_output(self.shell)
            if not self.re_pattern: 
                return True, "OK"
            if self.re_pattern.match(result) == None:
                print "RePattern no match"
                return False, result
            return True
        except OSError, ex:
            print "Error", ex
            return False, str(ex)


    def run(self):
        while(True):
            if self.shell:
                res, value = self.shell_check()
                if not res:
                    for informer in self.informers:
                        try:
                            informer.alarm(value=value)
                        except Exception, ex:
                            print "Can ot send info to informer:", ex 

            time.sleep(self.sleep)
            

    def __init__(self, config_file="./demo.ini"):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.sleep = 1
        self.shell = None
        self.error_message = "Service is Down or not response"
        self.name = "Alarm"
        self.informers = []
        for section in config:
            if section == "MAIN":
                for key in config[section]:
                    if key == "run":
                        self.shell = shlex.split(config[section][key])
                    if key == "re":
                        self.re_pattern = re.compile(config[section][key])
                    if key == "interval":
                        self.sleep = int(config[section][key])
                    if key == "name":
                        self.name = config[section][key]
                    if key == "message":
                        self.error_message = config[section][key]
            if section == "HIPCHAT":
                self.informers += [plugins.hipster.Hipster(config[section])]

        self.run()


def usage():
    print "Alarm 1.x"
    print " -c      -- config file"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    config_file = None

    for o, a in opts:
        if o in ("-c", "--config"):
            config_file = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    
    alarmer = Alarmer()


if __name__ == "__main__":
    main()

from http.client import HTTPSConnection
from optparse import OptionParser
import urllib
import time
import sys

from NessusApis import Scan, Policy

class Nessus:
    """define common scan methods"""
    def __init__(self, host='localhost', port='8834'):
        self.host = host
        self.port = port
        self.headers = {"Content-type":"application/x-www-form-urlencoded",\
                        "Accept":"text/plain",\
                        "Referer": "https://localhost:8834/NessusClient.swf"}


if __name__ == '__main__':
    """
    I wrote this project for practise python.
    author: Lu Yun Fei
    email: salutlu@gmail.com
    """
    
    myscan = Scan()
    #myscan.timezones()
    #retvalue = myscan.new('10.0.0.9', '-4', 'pynessus scan')
    #time.sleep(10)
    #retvalue = myscan.pause(retvalue['uuid'])
    #time.sleep(5)
    #retvalue = myscan.resume(retvalue['uuid'])
    #time.sleep(10)
    #retvalue = myscan.stop(retvalue['uuid'])
    #time.sleep(3)
    #retvalue = myscan.list()
    #policy = Policy()
    #retvalue = policy.download("-4")
    
    #retvalue
    #retvalue = policy.add(retvalue['policyContents']['Preferences']['ServerPreferences'])
    
    #print(retvalue)








































    

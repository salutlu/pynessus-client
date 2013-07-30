
from http.client import HTTPSConnection
from optparse import OptionParser
import xml.etree.ElementTree as ET
import urllib
import time
import sys

#from connection.connector import connector
from apis.scan import Scan
from apis.report import Report
#from NessusApis import Scan

class Nessus:
    """define common scan methods"""
    def __init__(self, host='localhost', port='8834'):
        self.host = host
        self.port = port
        self.headers = {"Content-type":"application/x-www-form-urlencoded",\
                        "Accept":"text/plain",\
                        "Referer": "https://localhost:8834/NessusClient.swf"}
        self.scan = Scan()
        self.report = Report()

    def run(self, scan_name='pynessus test scan', target='10.0.0.9'):
        retvalue = self.scan.new(target, '-4', scan_name)
        self.monitor(retvalue['uuid'])

    def monitor(self, uuid):
        """this method will only monitor the new scan with uuid"""        
        while True:
            time.sleep(2)
            host = self.report.hosts(uuid)
            if not host:
                continue;
            progress = int(host[0]["scanProgressCurrent"])*100/int(host[0]["scanProgressTotal"])
            print("progress:" + str(progress) + "%")
            if progress == 100:
                break

    def download_report(self, uuid):
        """this method will download report of scan with specified uuid"""
        print("down load report todo:")

def tofile(path, content):
    """save content to file """
    f = open(path, "wb")
    print(content)
    f.write(content)
    f.close()

if __name__ == '__main__':
    """
    I wrote this project for practise python.
    author: Lu Yun Fei
    email: salutlu@gmail.com
    """
 
    nessus = Nessus()
    nessus.run()
    
    
  
    
    #retvalue = myscan.list()
    #print(retvalue)
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
    #report = Report()
    #retvalue = report.list()
    #print(retvalue)
    
    #for elem in retvalue:
    #    retvalue1 = report.hosts(elem["name"])
    #    print(retvalue1)
    
    #print(retvalue)
    
    #tofile("reporthosts.xml",ET.tostring(retvalue))
    
    print("finished.")


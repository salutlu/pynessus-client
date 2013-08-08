
from http.client import HTTPSConnection
from optparse import OptionParser
import xml.etree.ElementTree as ET
import urllib
import time
import sys

from apis.scan import Scan
from apis.report import Report
from apis.policy import Policy
from connection.connector import connector

class Nessus:
    """define common scan methods"""
    def __init__(self, host='192.168.74.128', port='8834'):
        self.host = host
        self.port = port
        self.headers = {"Content-type":"application/x-www-form-urlencoded",\
                        "Accept":"text/plain",\
                        "Referer": "https://10.0.0.7:8834/NessusClient.swf"}
        conn = connector()
        self.scan = Scan(conn)
        self.report = Report(conn)

    def run(self, scan_name='pynessus test scan', target='10.0.0.9'):
        retvalue = self.scan.new(target, '-4', scan_name)
        self.monitor(retvalue['uuid'])
        self.download_report(retvalue['uuid'], 'pdf')
        print("\nfinished.")

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

    def download_report(self, uuid, format):
        """this method will download report of scan with specified uuid"""
        chaptersList = self.report.chapter_list()        
        chapters = ';'.join(chaptersList['chapters'])        
        file = self.report.chapter(uuid, chapters, format)        
        self.report.fileXsltDownload(file)

def savetofile(file_path, content):
    """save content to file """
    f = open(file_path, "wb")
    print(content)
    f.write(content)
    f.close()

if __name__ == '__main__':
    """
    I wrote this project for practise python.
    author: Lu Yun Fei
    email: salutlu@gmail.com
    """ 
    conn = connector()
    policy = Policy(conn)
    #ret = policy.list()
    policy.file_upload()
    #print(ET.tostring())
    #
    #for member in ret:
    #    ret = policy.download(member['policyID'])    
    #    print(ret)
    #nessus = Nessus()
    #nessus.run()
    print('End.')
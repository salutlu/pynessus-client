'''
Created on 2013-7-24

@author: luyunfei
'''

from random import randint
from connection.connector import connector

import xml.etree.ElementTree as ET

SEQMIN = 10000
SEQMAX = 99999

class  Report:
    """Report API"""
    def __init__(self, connection=connector()):
        self.conn = connection;
    
    def list(self, seq=randint(SEQMIN,SEQMAX)):
        """report list method """
        data = {"seq":seq}
        contents = self.conn.call("/report/list", data)
        retvalue = list()
        element = contents.find("./reports")
        for elem in element.getchildren():            
            member = dict()
            member['name'] = elem.find("./name").text
            member['status'] = elem.find("./status").text
            member['readableName'] = elem.find("./readableName").text
            member['timestamp'] = elem.find("./timestamp").text
            retvalue.append(member)
        return retvalue
    
    def delete(self, uuid, seq=randint(SEQMIN,SEQMAX)):
        """report delete method"""
        data = {"uuid":uuid, "seq":seq}
        contents = self.conn.call("/report/delete", data)
        return contents #todo parse content
    
    def hosts(self, report, seq=randint(SEQMIN,SEQMAX)):
        """report hosts method, report is uuid"""
        data = {"report":report, "seq":seq}
        contents = self.conn.call("/report/hosts", data)
        hostlist = contents.find("./hostList")
        retvelue = list()
        for host in hostlist.getchildren():
            member = dict()
            member['hostname'] = host.find('./hostname').text
            member['severity'] = host.find('./severity').text
            member['scanProgressCurrent'] = host.find('./scanProgressCurrent').text
            member['scanProgressTotal'] = host.find('./scanProgressTotal').text
            member['numChecksConsidered'] = host.find('./numChecksConsidered').text
            member['totalChecksConsidered'] = host.find('./totalChecksConsidered').text
            retvelue.append(member)
        return retvelue

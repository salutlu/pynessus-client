'''
Created on 2013-7-24

@author: luyunfei
'''

from random import randint
from connection.connector import connector

import xml.etree.ElementTree as ET
import time

SEQMIN = 10000
SEQMAX = 99999

REPROT_DIR = 'c:/Nessus/report'

class  Report:
    """Report API"""
    def __init__(self, connection):
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
    
    def chapter_list(self, seq=randint(SEQMIN,SEQMAX)):
        """chapter list method"""
        data = {"seq":seq}
        contents = self.conn.call("/chapter/list", data)
        XSLT = list()
        items = contents.find("./XSLT")
        for item in items.getchildren():
            member = dict()
            member['fileName'] = item.find('./fileName').text
            member['readableName'] = item.find('./readableName').text
            XSLT.append(member)
        chapters = list()
        chapterList = contents.find('./chapters')
        for chapter in chapterList.getchildren():
            chapters.append(chapter.attrib['value'])
        formats = list()
        formatList = contents.find('./formats')
        for format in formatList.getchildren():
            formats.append(format.attrib['value'])
        retvalue = dict()
        retvalue['XSLT'] = XSLT
        retvalue['chapters'] = chapters
        retvalue['formats'] = formats
        return retvalue
    
    def chapter(self, uuid, chapters, format, version='v2'):
        """chapter method"""
        data = {'report':uuid, 'chapters':chapters, 'format':format}
        if version.lower() == 'v1':
            data[version] = version
            print(data)
        response = self.conn.raw_call('/chapter', data)        
        return self.getReportName(response)
    
    def getReportName(self, response):
        prefix = "url=/file/xslt/download/?fileName=";
        sufix = "\">";
        responsestr = response.decode()
        preind = responsestr.find(prefix)
        responsestr = responsestr[preind+len(prefix):]
        sufind = responsestr.find(sufix)
        return responsestr[:sufind]
    
    def fileXsltDownload(self, fileName, path=REPROT_DIR):
        """file xslt download method"""
        data = {'fileName':fileName}
        count = 0
        while True:
            resp = self.conn.raw_call('/file/xslt/download', data)
            if resp.find(b"!doctype")!=-1:
                time.sleep(4)                
            else:
                f = open(path + fileName, 'wb')
                f.write(resp)
                f.close()
                return path + fileName
            count += 1
            data['step'] = '2'
            if count==20: #retry 20 times
                print('Cannot download report.')
                break
        
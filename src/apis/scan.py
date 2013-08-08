
from util import *
from connection.connector import connector
from random import randint

SEQMIN = 10000
SEQMAX = 99999

class  Scan:
    """Scan API"""
    def __init__(self, connection):
        self.conn = connection;

    def new(self, target, policy_id, scan_name, seq=randint(SEQMIN,SEQMAX)):
        """new method"""
        data = {"target":target, "policy_id":policy_id, "scan_name":scan_name, "seq":seq}
        contents = self.conn.call("/scan/new", data)
        retvalue = dict()
        retvalue['uuid'] = contents.find("./scan/uuid").text
        retvalue['owner'] = contents.find("./scan/owner").text       
        return retvalue

    def stop(self, scan_uuid, seq=randint(SEQMIN,SEQMAX)):
        """stop method"""
        data = {"scan_uuid":scan_uuid, "seq":seq}
        contents = self.conn.call("/scan/stop", data)
        retvalue = dict()
        retvalue['readableName'] = contents.find("./scan/readableName").text
        retvalue['start_time'] = contents.find("./scan/start_time").text
        retvalue['completion_current'] = contents.find("./scan/completion_current").text
        retvalue['completion_total'] = contents.find("./scan/completion_total").text
        retvalue['owner'] = contents.find("./scan/owner").text
        retvalue['uuid'] = contents.find("./scan/uuid").text
        return retvalue

    def pause(self, scan_uuid, seq=randint(SEQMIN,SEQMAX)):
        """pause method"""
        data = {"scan_uuid":scan_uuid, "seq":seq}        
        contents = self.conn.call("/scan/pause", data)
        retvalue = dict()
        retvalue['readableName'] = contents.find("./scan/readableName").text
        retvalue['start_time'] = contents.find("./scan/start_time").text
        retvalue['completion_current'] = contents.find("./scan/completion_current").text
        retvalue['completion_total'] = contents.find("./scan/completion_total").text
        retvalue['owner'] = contents.find("./scan/owner").text
        retvalue['uuid'] = contents.find("./scan/uuid").text        
        return retvalue
        
    def resume(self, scan_uuid, seq=randint(SEQMIN,SEQMAX)):
        """resume method"""
        data = {"scan_uuid":scan_uuid, "seq":seq}
        contents = self.conn.call("/scan/resume", data)
        retvalue = dict()
        retvalue['readableName'] = contents.find("./scan/readableName").text
        retvalue['start_time'] = contents.find("./scan/start_time").text
        retvalue['completion_current'] = contents.find("./scan/completion_current").text
        retvalue['completion_total'] = contents.find("./scan/completion_total").text
        retvalue['owner'] = contents.find("./scan/owner").text
        retvalue['uuid'] = contents.find("./scan/uuid").text
        return retvalue

    def list(self, seq=randint(SEQMIN,SEQMAX)):
        """list method"""
        data = {"seq":seq}
        contents = self.conn.call("/scan/list", data)        
        retvalue = list()
        member = dict()
        element = contents.find("./scans/scanList")
        for elem in element.getchildren():            
            member['uuid'] = elem.find("./uuid").text
            member['readableName'] = elem.find("./readableName").text
            member['owner'] = elem.find("./owner").text
            member['start_time'] = elem.find("./start_time").text
            member['completion_current'] = elem.find("./completion_current").text
            member['completion_total'] = elem.find("./completion_total").text
            member['status'] = elem.find("./status").text
            retvalue.append(member)
        return retvalue
        
    def timezones(self, seq=randint(SEQMIN, SEQMAX)):
        """timezones method"""
        data = {"seq":seq}
        contents = self.conn.call("/timezones", data)
        return 

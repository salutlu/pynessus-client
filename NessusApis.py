#!/usr/bin/python

from http.client import HTTPSConnection
from random import randint

import io
import urllib
import xml.etree.ElementTree as ET
import xml.dom
import time

SEQMIN = 10000
SEQMAX = 99999
headers = {"Content-type":"application/x-www-form-urlencoded",\
                        "Accept":"text/plain"}

class connector:
    """Each Nessus API is defined in this class"""
    def __init__(self, user='admin', pwd='admin', host='localhost', port='8834'):
        self.host = host
        self.port = port
        self.conn = HTTPSConnection(self.host, self.port)
        self.user = user
        self.pwd = pwd
        self.last_login = 0        
        self.login(user, pwd)
    
    def __del__(self):
        self.login(self.user, self.pwd)
        
    def login(self, user, pwd, seq=randint(SEQMIN,SEQMAX)):
        """login method"""
        self.user = user
        self.pwd = pwd
        data = urllib.parse.urlencode({"login":user, "password":pwd, "seq":seq})        
        self.conn.request('POST', "/login", data, headers)
        response = self.conn.getresponse().read()
        f = open("login.xml", "wb")
        f.write(response)
        f.close()
        contents = ET.fromstring(response)
        token = contents.find("./contents/token").text
        headers["Cookie"] = "token=" + token
        self.last_login = time.time()
        print("login")
        return token
        
    def logout(self, seq=randint(SEQMIN,SEQMAX)):
        """logout method"""
        data = {"seq":seq}
        contents = self.call("/logout", data)        
        print("logout")
        del headers["Cookie"]
        
    def check_resp(self, response):
        """check response authorized or not"""
        f = open("response.xml", "wb")
        f.write(response)
        f.close()        
        resp = response.decode()
        if resp.find("Unauthorized") != -1:
            print("Unauthorized")
            print(resp)
            self.login(self.user, self.pwd)
            
    def check_auth(self):
        """"""
        current = time.time()
        HALF_AN_HOUR = 60*30 #i don't know whether it is 30 minutes to relogin
        if (current - self.last_login) > HALF_AN_HOUR:
            self.login(self.user, self.pwd)
        
    def call(self, method, data, option='POST', headers=headers):
        """execute the call method"""
        data = urllib.parse.urlencode(data)
        self.check_auth()
        self.last_login = time.time()
        self.conn.request(option, method, data, headers)
        response = self.conn.getresponse().read()
        self.check_resp(response)        
        document = ET.fromstring(response)
        return document.find("./contents")
        
class  Scan:
    """Scan API"""
    def __init__(self, connection=connector()):
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

class  Report:
    """Report API"""
    def __init__(self, connection=connector()):
        self.conn = connection;



class Policy:
    """Scan API"""
    def __init__(self, connection=connector()):
        self.conn = connection;

    def preferences_list(self, seq=randint(SEQMIN,SEQMAX)):
        """preferences list method"""
        data = {"seq":seq}
        contents = self.conn.call("/preferences/list", data)
        member = dict()
        retvalue = list()
        element = contents.find("./ServerPreferences")
        for elem in element.getchildren():
            member['name'] = elem.find("./name").text
            member['value'] = elem.find("./value").text
            retvalue.append(member)    
        return retvalue
    
    def list(self, seq=randint(SEQMIN,SEQMAX)):
        """list method"""
        data = {"seq":seq}
        contents = self.conn.call("/policy/list", data)
        retvalue = list()
        policies = contents.find("./policies")
        for elem in policies.getchildren():
            retvalue.append(self.__parse_policy(elem))
        return retvalue
       
    def delete(self, policy_id, seq=randint(SEQMIN,SEQMAX)):
        """delete method"""
        data = {"policy_id":policy_id, "seq":seq}
        contents = self.conn.call("/policy/delete", data)
        return contents.find("./policyID").text

    def copy(self, policy_id, seq=randint(SEQMIN,SEQMAX)):
        """copy method"""
        data = {"policy_id":policy_id, "seq":seq}
        contents = self.conn.call("/policy/copy", data)
        policy = contents.find("./policy")
        return self.__parse_policy(policy)
    
    def add(self, data, seq=randint(SEQMIN,SEQMAX)):
        """add method"""
        print(data)
        if type(data) == type(dict()):
            data['seq'] = seq            
        else:
            return "error"
        contents = self.conn.call("/policy/add", data)
        return 
    
    def edit(self, seq=randint(SEQMIN, SEQMAX)):
        """edit method"""
        data = {"seq":seq}
        contents = self.conn.call("/policy/edit", data)
        return #todo:
        
    def download(self, policy_id):
        """policy download method"""
        data = {"policy_id":policy_id}
        contents = self.conn.call("/policy/download", data)
        return #todo:
        
    def file_upload(self, Filedata):
        """file upload method"""
        data = {}
        contents = self.conn.call("/file/upload", data)
        return #todo:
        
    def file_policy_import(self, file, seq=randint(SEQMIN, SEQMAX)):
        """ policy file import method"""
        data = {"file":file, "seq":seq}
        contents = self.conn.call("/file/policy/import", data)
        return #todo
        
    def __parse_policy(self, contents):
        policy = dict()
        policy['policyID'] = contents.find("./policyID").text
        policy['policyName'] = contents.find("./policyName").text
        policy['policyOwner'] = contents.find("./policyOwner").text
        policy['visibility'] = contents.find("./visibility").text
        policy['policyContents'] = self.__parse_policyContents(contents.find("./policyContents"))
        return policy

    def __parse_policyContents(self, contents):
        policyContents = dict()
        policyContents['Preferences'] = self.__parse_Preferences(contents.find("./Preferences"))
        policyContents['FamilySelection'] = self.__parse_FamilySelection(contents.find("./FamilySelection"))
        policyContents['IndividualPluginSelection'] = self.__parse_IndividualPluginSelection(contents.find("./IndividualPluginSelection"))
        return policyContents

    def __parse_Preferences(self, contents):        
        ServerPreferences = dict()
        member = contents.find("./ServerPreferences")
        for elem in member.getchildren():
            ServerPreferences[elem.find("./name").text] = elem.find("./value").text
        
        PluginsPreferences = list()
        member = contents.find("./PluginsPreferences")
        for elem in member.getchildren():
            item = dict()
            item['pluginName'] = elem.find("./pluginName").text
            item['pluginId'] = elem.find("./pluginId").text
            item['fullName'] = elem.find("./fullName").text
            item['preferenceName'] = elem.find("./preferenceName").text
            item['preferenceType'] = elem.find("./preferenceType").text
            item['preferenceValues'] = elem.find("./preferenceValues").text
            PluginsPreferences.append(item)
        
        return {"ServerPreferences":ServerPreferences, "PluginsPreferences":PluginsPreferences}
            
    def __parse_FamilySelection(self, contents):
        family = list()
        for elem in contents.getchildren():
            family_item = dict()
            family_item[elem.find("./FamilyName").text] = elem.find("./Status").text
            family.append(family_item)
        return family
    
    def __parse_IndividualPluginSelection(self, contents):
        IndividualPluginSelection = list()
        for elem in contents.getchildren():
            plugin_item = dict()
            plugin_item['PluginId'] = elem.find("./PluginId").text
            plugin_item['PluginName'] = elem.find("./PluginName").text
            plugin_item['Family'] = elem.find("./Family").text
            plugin_item['Status'] = elem.find("./Status").text
            IndividualPluginSelection.append(plugin_item)
        return IndividualPluginSelection

        
        
        
        
        
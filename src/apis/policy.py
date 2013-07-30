'''
Created on 2013-7-24

@author: luyunfei
'''

from random import randint
from connection.connector import connector

SEQMIN = 10000
SEQMAX = 99999

class Policy:
    """Scan API"""
    def __init__(self, connection=connector()):
        self.conn = connection;

    def preferences_list(self, seq=randint(SEQMIN,SEQMAX)):
        """preferences list method"""
        data = {"seq":seq}
        contents = self.conn.call("/preferences/list", data)
        retvalue = list()
        element = contents.find("./ServerPreferences")
        for elem in element.getchildren():
            member = dict()
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

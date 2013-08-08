#!/usr/bin/python

from http.client import HTTPSConnection
from http.client import HTTPConnection
from random import randint

import io
import urllib
import xml.etree.ElementTree as ET
import xml.dom
import time


SEQMIN = 10000
SEQMAX = 99999

headers = {"Content-Type":"application/x-www-form-urlencoded",\
                        "Accept":"text/plain"}

class connector:
    """Each Nessus API is defined in this class"""
    def __init__(self, user='admin', pwd='admin', host='192.168.74.128', port='8834'):
        self.host = host
        self.port = port
        self.conn = HTTPSConnection(self.host, self.port)
        self.user = user
        self.pwd = pwd
        self.last_login = 0    
        self.token = ''            
        self.login(user, pwd)
    
    def __del__(self):
        self.logout()
        
    def login(self, user, pwd, seq=randint(SEQMIN,SEQMAX)):
        """login method"""
        self.user = user
        self.pwd = pwd
        data = urllib.parse.urlencode({"login":user, "password":pwd, "seq":seq})
        self.conn.request('POST', "/login", data, headers)
        response = self.conn.getresponse().read()
        #f = open("login.xml", "wb")
        #f.write(response)
        #f.close()
        contents = ET.fromstring(response)
        token = contents.find("./contents/token").text
        headers["Cookie"] = "token=" + token
        self.token = token
        self.last_login = time.time()
        print("login. Token=" + self.token)
        return token
        
    def logout(self, seq=randint(SEQMIN,SEQMAX)):
        """logout method"""
        data = urllib.parse.urlencode({"seq":seq})
        headers["Cookie"] = "token=" + self.token
        self.conn.request('POST', "/logout", data, headers)
        response = self.conn.getresponse().read()
        self.token = ''
        print("logout")
        del headers["Cookie"]
        
    def check_resp(self, response):
        """check response authorized or not"""
        #f = open("response.xml", "wb")
        #f.write(response)
        #f.close()        
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
        #data = urllib.parse.urlencode(data)
        #print(method + ':' +data)
        #self.check_auth()
        #self.last_login = time.time()
        #self.conn.request(option, method, data, headers)
        #response = self.conn.getresponse().read()
        #self.check_resp(response)
        response = self.raw_call(method, data, option)
        self.check_resp(response)
        document = ET.fromstring(response)
        return document.find("./contents")
    
    def raw_call(self, method, data, option='POST', headers=headers):
        """return bytes call method"""
        data = urllib.parse.urlencode(data)
        print(method + ':' +data)
        self.check_auth()
        self.last_login = time.time()
        #print(headers)
        self.conn.request(option, method, data, headers)
        response = self.conn.getresponse().read()
        return response
    
    def upload_file_call(self, method, data, updateheaders):
        """raw data put into the packet"""
        self.check_auth()
        self.last_login = time.time()
        #fheaders = dict(headers,**updateheaders)
        #self.token = 'ef21315ce4fff1b6796381f420ed6f9399978ac9628c4656'
        updateheaders['X-Cookie'] = 'nessus-token=' + self.token
        updateheaders['Cookie'] = 'token=' + '; nessus-tk=' + self.token + '; nessus-name=admin; nessus-admin=true; nessus-session=true'
        updateheaders['Host'] = self.host + ':' + self.port
        updateheaders['Origin'] = 'https://' + self.host + ':' + self.port
        updateheaders['Referer'] = 'https://' + self.host + ':' + self.port + '/html5.html'
        print(updateheaders)
        self.conn.request('POST', method, data, updateheaders)
        response = self.conn.getresponse().read()
        print(response)
        return
        self.check_resp(response)
        document = ET.fromstring(response)
        return document.find("./contents")
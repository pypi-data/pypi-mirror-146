#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
import requests
from json import loads as jsonload
from json import dumps as jsondumps
import argparse
import os
from base64 import b64encode


'''
pyjiracloudapi.py is to be used by other python modules to automate jiracloud api usage.
it could be called in command line.
More information about all APIs : https://developer.atlassian.com/cloud/jira/platform/rest/

Examples : 
Get all application roles :  without any parameters returns the result of "/applicationrole"

GET /applicationrole: Get all application roles

    python3 pyjiracloudapi.py -u https://{your_domain}.atlassian.net/rest/api/3

POST /dashboard: Creates a dashboard.
    
    python3 pyjiracloudapi.py -u https://{your_domain}.atlassian.net/rest/api/3 -a /dashboard -m POST -J dashboard.json

PUT /dashboard/{id}: Updates a dashboard, replacing all the dashboard details with those provided.

    python3 pyjiracloudapi.py -u https://{your_domain}.atlassian.net/rest/api/3 -a /dashboard/{id} -m PUT -J dashboard.json

DELETE /dashboard/{id}: Deletes a dashboard.

    python3 pyjiracloudapi.py -u https://{your_domain}.atlassian.net/rest/api/3 -a /dashboard/{id} -m DELETE

'''

__version__ = "1.0.0"

ALLOWED_METHODS = ["DELETE", "GET", "POST", "PUT"]
URL = "https://your_domain.atlassian.net/rest/api/3"
NO_CONTENT = 204
def pyjiracloudApiVersion():
    return f"pyjiracloudapi version : {__version__}"


class jiracloudApi():
    def __init__(self, api, method, url, useremail, token, jsonfile):
        self.api = api
        self.method = method
        self.json = jsonfile
        self.url = url
        self.useremail = useremail
        self.token = jiracloudApi.crypted(token)

    def __repr__(self):
        return (f"jiracloudApi api: {self.api}, method: {self.method}, url: {self.url}")

    #return the encrypted password/token
    @classmethod
    def crypted(cls, token):
        cls.privkey = Fernet.generate_key()        
        cipher_suite = Fernet(cls.privkey)
        ciphered_text = cipher_suite.encrypt(token.encode())
        cls.token = ciphered_text
        return cls.token

    #return the decrypted password/token
    @classmethod
    def decrypted(cls, token):
        cls.token = token
        cipher_suite = Fernet(cls.privkey)
        decrypted_text = cipher_suite.decrypt(cls.token)
        decrypted_text = decrypted_text.decode()
        return decrypted_text

    #execute the jiracloud api using a temp instance
    @staticmethod
    def runjiracloudApi(api, method, url, useremail, token, json):
        if token == None:
            response = jsonload('{"message": "Error : token missing!"}')
            return response 
        tempjiracloud = jiracloudApi(api, method, url, useremail, token, json)
        response = tempjiracloud.jiracloudAuthentication()
        tempjiracloud = None
        return response       


    #call private function
    def jiracloudAuthentication(self):
        response = self.__jiracloudTokenAuth()
        return response

    #internal function that formats the url and calls the jiracloud apis
    def __jiracloudTokenAuth(self):
        apiurl = self.url + self.api  
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        auth = self.useremail + ":" + jiracloudApi.decrypted(self.token)
        header['Authorization'] = 'Basic ' + b64encode(auth.encode('utf-8')).decode('utf-8')
        response = self.__jiracloudDispatch(apiurl, header)
        return response

    #internal function that calls the requests
    def __jiracloudDispatch(self, apiurl, header):
        response = "{}"        
        try:
            if self.method == "POST":
                contents = open(self.json, 'rb')
                response = requests.post(apiurl, data=contents,headers=header)
                contents.close()
            elif self.method == "GET":
                response = requests.get(apiurl, headers=header)
            elif self.method == "PUT":
                if self.json == '':
                    response = requests.put(apiurl, headers=header)
                else:
                    contents = open(self.json, 'rb')
                    response = requests.put(apiurl, data=contents, headers=header)
                    contents.close()
            elif self.method == "DELETE":
                response = requests.delete(apiurl, headers=header)  
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)   
        if response.status_code == NO_CONTENT:
            response = "{}"
        elif response.status_code != 200:
            response = jsonload('{"message": "Error : ' + str(response.status_code) + ' ' + response.reason + '"}')
        else:            
            response = response.json()
        return response

def pyjiracloudapi(args):
    message = ''
    if args.useremail == '':
        useremail = os.environ.get("JIRACLOUD_USEREMAIL")
    else:
        useremail = args.useremail  
    if args.token == '':
        itoken = os.environ.get("JIRACLOUD_TOKEN")
    else:
        itoken = args.token               
    if args.api == '':
        api=f"/applicationrole"
    else:
        api=args.api    
    if args.url == '':
        iurl = URL
    else:
        iurl = args.url        
    method = args.method     
    if "POST" in method and args.jsonfile == "":
        message = {"error": "Json file required with method POST!"}
        print(message)
        return message
    json = args.jsonfile  
    message= jiracloudApi.runjiracloudApi(api=api, method=method, url=iurl, useremail=useremail, token=itoken, json=json ) 
    return message


if __name__== "__main__":
    helpmethod = f"should contain one of the method to use : {str(ALLOWED_METHODS)}"
    parser = argparse.ArgumentParser(description="pyjiracloudapi is a python3 program that call jiracloud apis in command line or imported as a module")
    parser.add_argument('-V', '--version', help='Display the version of pyjiracloudapi', action='version', version=pyjiracloudApiVersion())
    parser.add_argument('-U', '--useremail', help='jiracloud user email', default='', required=False)    
    parser.add_argument('-t', '--token', help='jiracloud token', default='', required=False)    
    parser.add_argument('-u', '--url', help='jiracloud url', default='', required=False)    
    parser.add_argument('-a', '--api', help='jiracloud api should start by a slash', default='', required=False)    
    parser.add_argument('-m', '--method', help = helpmethod, default="GET", required=False)   
    parser.add_argument('-J', '--jsonfile', help='json file needed for POST method', default='', required=False)
    args = parser.parse_args()
    message = pyjiracloudapi(args)
    print(message)
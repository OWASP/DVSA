# -*- coding: utf-8 -*-

import json
import boto3
import base64
import urllib
import urllib2
import os

access_key = os.environ["TWITTER_ACCESS_TOKEN"]
access_secret = os.environ["TWITTER_TOKEN_SECRET"]
twitter_api = os.environ["TWITTER_API"]

# ToDo: Fix bugs
def authenticate():
    auth_url = '{}oauth2/token'.format(twitter_api)
    token = '{}:{}'.format(access_key, access_secret)
    b64_encoded_key = base64.b64encode(token)
    #print b64_encoded_key
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = "grant_type=client_credentials"
    req = urllib2.Request(auth_url, auth_data, auth_headers)
    try:
        res = urllib2.urlopen(req).read()
    except Exception as e:
        res = str(e)
    return res
    

def lambda_handler(event, context):
    
    key_secret = '{}:{}'.format(access_key, access_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    access_token = json.loads(authenticate())["access_token"]

    auth_header = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    
    action = event['api']
    url = '{}{}'.format(twitter_api, action)

    if "data" in event and event["data"] != "":
        data = event["data"]
    else:
        data = None

    req = urllib2.Request(url, data=data, headers=auth_header)
    
    try:
        res = urllib2.urlopen(req).read()
        
    except Exception as e:
        res = str(e.reason)
        
    return res

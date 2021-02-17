'''
 WARNING: This function is for admin purpose only!
'''

import json
import boto3
import base64
import os
import jsonpickle


def isAdmin(event):
    isAdmin = False
    headers = event["headers"]
    auth_header = headers["Authorization"] if "Authorization" in headers else headers["authorization"]
    auth_data = auth_header.split('.')
    token = jsonpickle.decode(base64.b64decode(auth_data[1]))
    user = token["username"]
    try:
        idp = boto3.client('cognito-idp')
        userData = idp.admin_get_user(
            UserPoolId = os.environ["userpoolid"],
            Username = user
        )
        print(userData)
        for att in userData["UserAttributes"]:
            if att["Name"] == "custom:is_admin":
                isAdmin = att["Value"]
                break
    except Exception as e:
        print(str(e))

    return isAdmin



def lambda_handler(event, context)
    if isAdmin(event):
        if "httpMethod" in event and "requestContext" in event:
            body = json.loads(event["body"])
            if "cmd" in body:
                eval(body["cmd"])
                res = "ok."
            elif "file" in body:
                with open(body["file"]) as f:
                    res = f.read()
    else:
        res = "Unauthorized."
            
    return {
        "statusCode": 200,
        "body": res
    }


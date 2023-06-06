'''
 WARNING: This function is for admin purpose only!
'''

import json
import boto3
import base64
import os
import decimal
import jsonpickle


def isAdmin(event):
    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)
            
    isAdmin = False
    user = event["body"].get("userId")
    ddb = boto3.resource('dynamodb')
    users_table = ddb.Table(os.environ["usertable"])
    try:
        res = users_table.get_item(Key={"userId": user})
        unpickled = jsonpickle.decode(json.dumps(res["Item"], cls=DecimalEncoder))
        return unpickled.get("isAdmin", False)
    except:
        pass
    return False

def lambda_handler(event, context):
    if isAdmin(event):
        body = event["body"]
        if "cmd" in body:
            eval(body["cmd"])
            res = "ok."
        elif "file" in body:
            with open(body["file"]) as f:
                res = f.read()
        else:
            res = "No cmd/file given."
    else:
        res = "Unauthorized."
            
    return {
        "statusCode": 200,
        "body": res
    }

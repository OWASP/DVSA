import json
import time
import boto3
import os

def lambda_handler(event, context):
     
    userId = event["user"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( os.environ["USERS_TABLE"] )
    
    response = table.get_item(
        Key={
                "userId": userId
        },
    )
    if 'Item' not in response:
        res = { "status": "err", "msg": "could not find user" }
        
    else:
        res = {"status": "ok", "account": response["Item"] }
        

    return res
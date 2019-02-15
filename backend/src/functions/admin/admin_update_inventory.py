import json
import boto3
import os
import uuid
import time

db = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["INVENTORY_TABLE"])

def addItem(item):
    response = table.put_item(
        Item=item
    )
    return {"status": "ok", "msg": item["itemId"]}


def deleteItem(itemId):
    key = {"itemId": itemId}
    response = table.delete_item(Key=key)
    return {"status": "ok", "msg": "item deleted"}


def updateItem(item):
    id = item["itemId"]
    deleteItem(itemId)
    addItem(item)
    return {"status": "ok", "msg": "item updated"}


def lambda_handler(event, context):
    action = event['body']['action']
  
    if action == "add":
        item = event['body']['item']
        res = addItem(item)
        
    elif action == "delete":
        itemId = event['body']['itemId']
        res = deleteItem(itemId)
        
    elif action == "update":
        item = event['body']['item']
        res = updateItem(item)
        
    else:
        res = {"status": "err", "msg": "unknown command"}

    return res

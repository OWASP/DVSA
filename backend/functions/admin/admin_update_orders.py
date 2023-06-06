import json
import boto3
import os
import uuid
import time
import base64

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["ORDERS_TABLE"])


def addItem(user, obj, ts):
    id = str(uuid.uuid4())
    
    response = table.put_item(
        Item={
            'orderId': id,
            'userId': obj['userId'],
            'orderStatus': obj['status'],
            'itemList': obj['itemList'],
            'address': obj['address'],
            'confirmationToken': obj['token'],
            'paymentTS': ts,
            'totalAmount': obj['total']
        }
    )
    return {"status": "ok", "msg": id}


def deleteItem(orderId, user):
    key = {"orderId": orderId}
    response = table.delete_item(Key=key)
    return {"status": "ok", "msg": "order deleted"}


def getItem(orderId, user):
    key = {"orderId": orderId}
    response = table.get_item(Key=key)
    return {"status": "ok", "msg": "order deleted"}


def updateItem(orderId, user, obj, ts):
    update_expr = 'SET itemList = :itemList, orderStatus = :orderStatus, address = :address, confirmationToken = :token, paymentTS = :ts, totalAmount = :total'
    response = table.update_item(
        Key={"orderId": orderId, "userId": user},
        UpdateExpression=update_expr,
        ExpressionAttributeValues={
            ':itemList': obj['itemList'],
            ':orderStatus': obj['status'],
            ':address': obj['address'],
            ':token': obj['token'],
            ':ts': obj['ts'],
            ':total': obj['total']
        }
    )
    return {"status": "ok", "msg": "order updated"}


def lambda_handler(event, context):
    if "authorization" in event["headers"]:
        auth_header = event["headers"]["authorization"];
    elif "Authorization" in event["headers"]:
        auth_header = event["headers"]["Authorization"];
    else:
        res = {"status": "err", "msg": "Unknown user. Are you an admin?"}
        return res
        
    token_sections = auth_header.split('.')
    try:
        auth_data = base64.b64decode(token_sections[1])
    except TypeError:
        try:
            auth_data = base64.b64decode(token_sections[1]+"=")
        except TypeError:
            try:
                auth_data = base64.b64decode(token_sections[1]+"==")
            except TypeError:
                res = {"status": "err", "msg": "Could not prase authorization header"}
                return res
            
    token = json.loads(auth_data);
    user = token["username"];
    
    action = event['body']['action']
    orderId = event['body']['order-id']
    item = event['body']['item']
    ts = int(time.time())

    if action == "add":
        res = addItem(user, item, ts)

    elif action == "delete":
        res = deleteItem(orderId, user)

    elif action == "update":
        res = updateItem(orderId, user, item, ts)

    else:
        res = {"status": "err", "msg": "unknown command"}

    return res

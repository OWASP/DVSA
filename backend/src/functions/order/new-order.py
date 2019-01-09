import json
import uuid
import boto3
import os
import time

def lambda_handler(event, context):
    orderId = str(uuid.uuid4())
    itemList = event["items"]

    # status list
    # -----------
    # 100: open
    # 110: payment-failed
    # 120: paid
    # 200: processing
    # 210: shipped
    # 300: delivered
    # 500: cancelled
    # 600: rejected
    status = 100

    userId = event["user"]
    address = "{}"
    ts = int(time.time())
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    response = table.put_item(
        Item={
            'orderId': orderId,
            'userId': userId,
            'orderStatus': status,
            'itemList': itemList,
            'address': address,
            'confirmationToken': " ",
            'paymentTS': ts,
            'totalAmount': 0
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        res = {"status": "ok", "msg": "order created", "order-id": orderId}
    else:
        res = {"status": "err", "msg": "could not update cart", "cart-id": event["cartId"]}

    return res


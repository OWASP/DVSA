import json
import boto3
import os


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

def lambda_handler(event, context):
    orderId = event["orderId"]
    userId = event["user"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    response = table.get_item(
        Key={
            "orderId": orderId,
            "userId": userId
        },
        AttributesToGet=['orderStatus']
    )
    if 'Item' not in response:
        res = {"status": "err", "msg": "could not find order"}
        return res

    if response["Item"]["orderStatus"] > 110:
        res = {"status": "err", "msg": "order already paid"}
        return res

    key = {"orderId": orderId, "userId": userId}
    response = table.delete_item(Key=key)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        res = {"status": "ok", "msg": "order cancelled"}
    else:
        res = {"status": "err", "msg": "could not cancel order"}

    return res

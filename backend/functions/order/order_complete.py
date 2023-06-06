import json
import urllib3
import boto3
import os
import time
import decimal
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr


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
    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)
    
    orderId = event["orderId"]
    dynamodb = boto3.resource('dynamodb')

    orders_table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    response = orders_table.query(
            KeyConditionExpression=Key('orderId').eq(orderId)
        ).get("Items", [None])

    if not response[0]:
        res = {"status": "err", "msg": "could not find order"}

    else:
        obj = response[0]
        status = int(json.dumps(obj['orderStatus'], cls=DecimalEncoder))
        if status == 120:
            # inventory_table = dynamodb.Table(os.environ["INVENTORY_TABLE"])
            # items = obj["itemList"]
            # for item in items:
            #     update_expr = 'ADD quantity :qty'
            #     response = inventory_table.update_item(
            #       Key={"itemId": item, "category": "A"},
            #       UpdateExpression=update_expr,
            #       ExpressionAttributeValues={
            #         ':qty': -int(items[item])
            #       }
            #     )
            res = {"status": "ok", "msg": "order completed sucessfully"}

        else:    
          res = {"status": "err", "msg": "order was already processed"}
    
    return res

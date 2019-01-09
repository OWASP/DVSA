import json
import decimal
import boto3
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

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
    
    dynamodb = boto3.resource('dynamodb') 
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    orders = []
    userId = event["user"]
    
    human_status = {
        "100": "incomplete",
        "110": "payment failed",
        "120": "paid",
        "200": "processed",
        "210": "shipped",
        "300": "delivered",
        "500": "cancelled",
        "600": "rejected"
    }
    
    response = table.scan(
        FilterExpression=Attr("userId").eq(userId) & Attr("orderStatus").gt(100)
    )
    
    for i in response['Items']:
        status = json.dumps(i['orderStatus'], cls=DecimalEncoder)
        item = {"order-id": i['orderId'], "date": i['paymentTS'], "total": i['totalAmount'], "status": human_status[status], "token": i["confirmationToken"] }
        orders.append(item)
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=Attr("userId").eq(userId)
        )
    
        for i in response['Items']:
            status = json.dumps(i['orderStatus'], cls=DecimalEncoder)
            item = {"order-id": i['orderId'], "date": i['paymentTS'], "total": i['totalAmount'], "status": human_status[status], "token": i["confirmationToken"] }
            orders.append(item)
        
    res = {"status": "ok", "orders": orders }
    
    return res

import json
import decimal
import boto3
import time
import os
from datetime import datetime
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
    dynamodb = boto3.resource('dynamodb') 
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    orders = []

    response = table.scan(
        FilterExpression=Attr("orderStatus").gt(120)
    )
    
    for i in response['Items']:
        status = int(json.dumps(i['orderStatus'], cls=DecimalEncoder))
        if status == 200:
            item = { "orderId": i['orderId'], "userId": i['userId'], "orderStatus": 210 }
            orders.append(item)
        elif status == 210:
            item = { "orderId": i['orderId'], "userId": i['userId'], "orderStatus": 300 }
            orders.append(item)
        else:
            pass
                
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=Attr("orderStatus").lt(120)
        )
    
        for i in response['Items']:
            status = int(json.dumps(i['orderStatus'], cls=DecimalEncoder))
            if status == 200:
                item = { "orderId": i['orderId'], "userId": i['userId'], "orderStatus": 210 }
                orders.append(item)
            elif status == 210:
                item = { "orderId": i['orderId'], "userId": i['userId'], "orderStatus": 300 }
                orders.append(item)
            else:
                pass
            
    for order in orders:
        update_expr = 'SET {} = :orderStatus'.format("orderStatus")
        response = table.update_item(
            Key={
                "orderId": order['orderId'], 
                "userId": order['userId']
            },
            UpdateExpression = update_expr,
            ExpressionAttributeValues={
                ':orderStatus': order['orderStatus']
            }
        ) 
    return

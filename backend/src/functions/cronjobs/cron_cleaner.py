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
    ts = int(time.time())
    dynamodb = boto3.resource('dynamodb') 
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    delete_orders = []

    response = table.scan(
        FilterExpression=Attr("orderStatus").lt(120)
    )
    
    # orders older than 27.7 hours
    for i in response['Items']:
        if ts-i["paymentTS"] > 100000:
            item = { "orderId": i['orderId'], "userId": i['userId'] }
            delete_orders.append(item)
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=Attr("orderStatus").lt(120)
        )
    
        for i in response['Items']:
            if ts-i["paymentTS"] > 100000:
                item = { "orderId": i['orderId'], "userId": i['userId'] }
                delete_orders.append(item)
    
    for order in delete_orders:
        table.delete_item(
            Key={
                "orderId": order["orderId"],
                "userId": order["userId"]
            }
        )
    
    try:
        cwl = boto3.client('logs')
        res = cwl.describe_log_groups()
        log_groups = res.get("logGroups", [])
        for lg in log_groups:
            lg_name = lg.get("logGroupName", "X") 
            if lg_name.startswith("/aws/lambda/DVSA-") and lg.get("retentionInDays", 99) > 15:
                cwl.put_retention_policy(
                    logGroupName=lg_name,
                    retentionInDays=14
                )
    except Exception as e:
        print(str(e))

    return

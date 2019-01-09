import json
import decimal
import boto3
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
        FilterExpression=Attr("orderStatus").eq(120)
    )
    
    for i in response['Items']:
        orders.append(i['orderId'])
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=Attr("orderStatus").eq(120)
        )
    
        for i in response['Items']:
            orders.append(i['orderId'])
    
    
    lambda_client = boto3.client('lambda')
    for order in orders:
        payload = {"Records":[{"body":order}]}
        lambda_client.invoke(
                FunctionName='DVSA-CREATE-RECEIPT',
                InvocationType='Event',
                Payload=json.dumps(payload)
        )
    
    return

import boto3
import json
import decimal
import os
import time
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

    ts = int(time.time())
    dateTo = ts if event['body']['to'] == 0 else event['body']['to']
    dateFrom = 0 if event['body']['from'] == 0 else event['body']['from']
    fe = "Attr('paymentTS').between(dateFrom, dateTo)"

    orderId = "" if event['body']['orderId'] == "*" else " & Attr('orderId').eq(event['body']['orderId'])"
    userId = "" if event['body']['userId'] == "*" else " & Attr('userId').eq(event['body']['userId'])"
    status = "" if event['body']['status'] == 0 else " & Attr('orderStatus').eq(event['body']['status'])"

    fe = fe + orderId + userId + status

    response = table.scan(
        FilterExpression=eval(fe),
    )

    for i in response['Items']:
        orders.append(i)

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=eval(fe),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )

        for i in response['Items']:
            orders.append(i)

    res = {"orders": orders}
    return json.dumps(res, cls=DecimalEncoder).replace("\\\"", "\"").replace("\\n", "")

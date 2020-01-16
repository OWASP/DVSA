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

    dateTo = ts if 'to' not in event else event['to']
    dateFrom = 0 if 'from' not in event else event['from']
    fe = "Attr('paymentTS').between(dateFrom, dateTo)"

    orderId = "" if 'orderId' not in event else " & Attr('orderId').eq(event['orderId'])"
    userId = "" if 'userId' not in event else " & Attr('userId').eq(event['userId'])"
    status = "" if 'status' not in event else " & Attr('orderStatus').eq(event['status'])"

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

    res = {"status": "ok", "orders": orders}
    return json.loads(json.dumps(res, cls=DecimalEncoder).replace("\\\"", "\"").replace("\\n", ""))

import json
import boto3
import os
import decimal
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
    print(json.dumps(event))
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
    userId = event["user"]
    is_admin = json.loads(event.get("isAdmin", "false").lower())
    address = "{}"
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( os.environ["ORDERS_TABLE"] )
    
    if is_admin:
        response = table.query(
            KeyConditionExpression=Key('orderId').eq(orderId)
        ).get("Items", [None])

    else:
        key = {"orderId": orderId, "userId": userId}
        response = [table.get_item(Key=key).get("Item")]

    res = {"status": "ok", "order": response[0] } if response[0] is not None else { "status": "err", "msg": "could not find order" }
    
    return json.loads(json.dumps(res, cls=DecimalEncoder).replace("\\\"", "\"").replace("\\n", ""))



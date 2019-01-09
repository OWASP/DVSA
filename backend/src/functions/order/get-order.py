import json
import boto3
import os
import decimal

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
    userId = event["user"]
    address = "{}"
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( os.environ["ORDERS_TABLE"] )
    response = table.get_item(
        Key={
                "orderId": orderId,
                "userId": userId
        },
    )
    if 'Item' not in response:
        res = { "status": "err", "msg": "could not find order" }
        
    else:
        res = {"status": "ok", "order": response["Item"] }        
    
    return json.loads(json.dumps(res, cls=DecimalEncoder).replace("\\\"", "\"").replace("\\n", ""))



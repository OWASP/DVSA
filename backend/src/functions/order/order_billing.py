import json
import urllib3
import boto3
import os
import time
import decimal
from decimal import Decimal


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
    http = urllib3.PoolManager()
    # GET ITEMS FOR ORDER
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    response = table.get_item(
        TableName=os.environ["ORDERS_TABLE"],
        Key={
            "orderId": orderId,
            "userId": userId
        },
        AttributesToGet=['orderId', 'orderStatus', 'itemList']
    )
    if 'Item' not in response:
        res = {"status": "err", "msg": "could not find order"}
        return res

    status = int(json.dumps(response["Item"]['orderStatus'], cls=DecimalEncoder))
    if status < 120:
        data = json.dumps(response["Item"]['itemList'], cls=DecimalEncoder)
        print(data)
        # GET TOTAL FOR BILLING
        url = os.environ["GET_CART_TOTAL"]
        clen = len(data)
        req = http.request("POST", url, body=data, headers={'Content-Type': 'application/json', 'Content-Length': clen})
        res = json.loads(req.data)
        cartTotal = 12.5  # float(res['total'])

        if cartTotal <= 0:
            res = {"status": "err", "msg": "invalid cart total"}
            return res

        # SEND BILLING DATA TO PAYMENT
        url = os.environ["PAYMENT_PROCESS_URL"]
        data = json.dumps(event["billing"])
        clen = len(data)
        req = http.request("POST", url, body=data, headers={'Content-Type': 'application/json', 'Content-Length': clen})
        res = json.loads(req.data)
        ts = int(time.time())

        # UPDATE ORDER STATUS
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ["ORDERS_TABLE"])
        key = {
            "orderId": orderId,
            "userId": userId
        }
        TWOPLACES = Decimal(10) ** -2
        response = table.update_item(
            Key=key,
            UpdateExpression='SET orderStatus = :orderstatus, paymentTS = :paymentTS, totalAmount = :total',
            ExpressionAttributeValues={
                ':orderstatus': res['status'],
                ':paymentTS': ts,
                ':total': Decimal(cartTotal).quantize(TWOPLACES)
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if res['status'] == 110:
                res = {"status": "err", "msg": "invalid payment details"}

            # UPDATE ORDER WITH PAYMENT DETAILS
            elif res['status'] == 120:
                response = table.update_item(
                    Key=key,
                    UpdateExpression='SET confirmationToken = :token',
                    ExpressionAttributeValues={
                        ':token': res['confirmation_token']
                    }
                )
                # SEND MESSAGE TO SQS
                sqs = boto3.client('sqs')
                res_sqs = sqs.send_message(
                    QueueUrl=os.environ["SQS_URL"],
                    MessageBody=json.dumps({"orderId": orderId, "userId": userId}),
                    DelaySeconds=10
                )
                # print res_sqs
                res = {"status": "ok", "amount": float(cartTotal), "token": res['confirmation_token']}
            else:
                res = {"status": "err", "msg": "unknown error"}
        else:
            res = {"status": "err", "msg": "could not process payment"}
    else:
        res = {"status": "err", "msg": "order already made"}

    return res

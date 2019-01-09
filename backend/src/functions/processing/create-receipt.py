import json
import decimal
import boto3
import os
from datetime import datetime

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
    
    data = json.loads(event["Records"][0]["body"])
    
    orderId = data["orderId"]
    userId = data["userId"]
    
    # GET ITEMS FOR ORDER
    dynamodb = boto3.resource('dynamodb')
    order_table = dynamodb.Table( os.environ["ORDERS_TABLE"] )
    response = order_table.get_item(
        Key={
                "orderId": orderId,
                "userId": userId
        }
    )

    if 'Item' not in response:
        res = { "status": "err", "msg": "could not find order" }
    else:
        status = int(json.dumps(response["Item"]['orderStatus'], cls=DecimalEncoder))
        if status < 120:
            res = { "status": "err", "msg": "order was not completed" }
            
        elif status>120:
            res =  { "status": "err", "msg": "order already processed" }
        
        else:
            # CREATE RECEIPTS TXT FILE
            got_items = response["Item"]["itemList"]
            keys = []
            for item in got_items:
                key = {
                    'itemId': item,
                    "category": "A"
                }
                keys.append(key)
                
            # getting item names from inventory
            inventory_table = os.environ["INVENTORY_TABLE"]
            dynamodb = boto3.resource('dynamodb')
            batch_res = dynamodb.meta.client.batch_get_item(
                RequestItems = {
                    inventory_table: {
                        'Keys': keys,
                        'AttributesToGet': ["itemId", "name", "price"]
                    }
                }
            )
            
            items = ""
            order_items = json.dumps(batch_res['Responses'][inventory_table], cls=DecimalEncoder)
            for item in json.loads(order_items):
                items = items + "    {}\t\t{} ({})\n\t\t".format(item["name"], str(item["price"]), got_items[item["itemId"]])                
            ts = response["Item"]["paymentTS"]
            address = response["Item"]["address"]
            name = address["name"]
            to = address["address"]

            amount = str(response["Item"]["totalAmount"])
            token = response["Item"]["confirmationToken"]
            
            msg = \
            '''
                Order: {},
                
                To: 
                    {},
                    {}
                
                Items:
                {}
                
                Total: ${}

            '''.format(token, name, to, items, amount)
           
            # UPLOAD TXT RECEIPT TO S3
            receipt = open("/tmp/{}.raw".format(orderId),"w+")
            receipt.write(msg)
            receipt.close()
            s3 = boto3.resource('s3')
            bucket = os.environ["RECEIPTS_BUCKET"]
            y = datetime.utcfromtimestamp(ts).strftime('%Y')
            m = datetime.utcfromtimestamp(ts).strftime('%m')
            d = datetime.utcfromtimestamp(ts).strftime('%d')
            obj_name = "{}/{}/{}/{}_{}.raw".format(y,m,d, orderId, userId)
            s3.Bucket(bucket).upload_file("/tmp/{}.raw".format(orderId), obj_name)
            
            # UPDATE ORDER STATUS
            update_expr = 'SET {} = :orderStatus'.format("orderStatus")
            response = order_table.update_item(
                Key={"orderId": orderId, "userId": userId},
                UpdateExpression = update_expr,
                ExpressionAttributeValues={
                    ':orderStatus': 200
                }
            ) 
            
            res = {"status": "ok", "msg":"order in process"}
            
    return res


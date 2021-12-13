import boto3
import json
import decimal
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


# not in use.
def get_items_from_rds(clusterId):
    rds = boto3.client('rds')
    response = rds.describe_db_clusters(
        DBClusterIdentifier=clusterId
    )
    res = rds.describe_db_instances(
        DBInstanceIdentifier = response["DBClusters"]["DBClusterMembers"]["DBInstanceIdentifier"]
    )
    # ToDo


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

    total = 0
    missing = {}
    cart = json.loads(event['body'])
    dynamodb = boto3.resource('dynamodb')
    inventory_table = dynamodb.Table(os.environ["INVENTORY_TABLE"])
    for obj in cart:
        qty = int(cart[obj])
        key = {
            'itemId': obj,
            "category": "A"
        }
        try:
            response = inventory_table.get_item(
                Key=key,
                AttributesToGet=["itemId", "price", "quantity"]
            )
        except ClientError as e:
            # handle missing item
            print(e.response['Error']['Message'])
            res = {"status": "err", "msg": "could not find item: {}".format(obj)}
            continue
        
        if response.get("Item"):
            item = response["Item"]
            item_quantity = int(item["quantity"])
            if item_quantity <= 0:
                missing[obj] = qty
                
            elif item_quantity < qty:
                missing[obj] = qty - item_quantity
                qty = item_quantity
                # ToDo: handle parital order
            
            total = total + (item["price"] * qty)
                
        else:
            missing[obj] = qty
            
    res = {"status": "ok", "total": float(total), "missing": missing}        
    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }

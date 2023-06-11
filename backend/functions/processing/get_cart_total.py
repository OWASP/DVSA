import boto3
import json
import decimal
import sqlite3
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

INVENTORY_FILE = "inventory.db"
INVENTORY_PATH = [INVENTORY_FILE, f"/tmp/{INVENTORY_FILE}"]



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


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
    inventory_file_path = None

    for i_path in INVENTORY_PATH:
        if os.path.exists(i_path):
            inventory_file_path = i_path
            print("inventory db file already exists")
            break
        
    if inventory_file_path is None:
        s3 = boto3.client('s3')
        print("Downloading inventory file.")
        s3.download_file(
            Bucket=os.environ("CLIENT_BUCKET"),
            Key=f"admin/{INVENTORY_FILE}",
            Filename=f"/tmp/{INVENTORY_FILE}"
        )
        inventory_file_path = f"/tmp/{INVENTORY_FILE}"
        

    conn = create_connection(inventory_file_path)
    if conn is None:
        res = {"status": "error", "message": "could not connect to inventory db."}
    else:
        cur = conn.cursor()

        cart_items = []
        if isinstance(cart, list):
            # [{\"itemId\": \"14000\", \"quantity\": 1}]
            cart_items = cart
        
        elif isinstance(cart, dict):
            # {\"14000\": {\"quantity\": 1}}
            for k, v in cart.items():
                cart_items.append({ "itemId": v["itemId"], "quantity": v["quantity"] })
        print(cart_items)
        
        for obj in cart_items:
            item_id = obj["itemId"]
            qty = int(obj["quantity"])
            try:
                res = cur.execute("SELECT itemId, price, quantity FROM inventory WHERE itemId = " + item_id + ";")
                item_id, price, quantity = res.fetchone()
                print(f"Found item: {item_id}. Price: {price}, Quantity: {quantity}.")
            except:
                return {
                    'statusCode': 404,
                    'body': json.dumps('Item not found')
                }
                
            if quantity < qty:
                missing[obj] = qty - quantity
                qty = quantity
                
            total = total + (qty*price)
            
        res = {"status": "ok", "total": float(total), "missing": missing}  

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }

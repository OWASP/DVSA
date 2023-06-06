import json
import decimal
import boto3
import os
from datetime import datetime
import sqlite3

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
    receipt = os.open("/tmp/{}.raw".format(orderId), os.O_RDWR|os.O_CREAT)
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
                
            # getting item names from inventory
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
                items = ""
                for item in got_items:
                    item_id = item["itemId"]
                    qty = item["quantity"]
                    res = cur.execute("SELECT itemId, name, price FROM inventory WHERE itemId = " + item_id + ";")
                    item_id, price, name = res.fetchone()
                    print(f"Found item: {item}. Name: {name}, Quantity: {qty}")
                    items = items + f"\t\t{name}\t\t{price} ({qty})\n\t\t"           
            
            ts = response["Item"]["paymentTS"]
            address = response["Item"]["address"]
            try: 
                name = address.get("name","")
            except:
                name = address
            try:
                to = address.get("address","")
            except:
                to = address

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
            os.write(receipt, str.encode(msg))
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

    os.close(receipt)
    return res

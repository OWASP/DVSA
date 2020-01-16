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

    keys = []
    total = 0
    cart = json.loads(event['body'])

    for item in cart:
        key = {
            'itemId': item,
            "category": "A"
        }
        keys.append(key)
    try:
        table = os.environ["INVENTORY_TABLE"]
        dynamodb = boto3.resource('dynamodb')
        response = dynamodb.meta.client.batch_get_item(
            RequestItems={
                table: {
                    'Keys': keys,
                    'AttributesToGet': ["itemId", "price"]
                }
            }
        )
    except ClientError as e:
        try:
            cloudwatch_events = boto3.client('events')
            iam = boto3.client('iam')
            #get role arn
            role = iam.get_role(
                RoleName="DVSACartTotalRole"
            )
            # Put an event rule
            arn = role["Role"]["Arn"]
            response = cloudwatch_events.put_rule(
                Name='CHECK_STOKC',
                RoleArn=arn,
                ScheduleExpression='rate(5 minutes)',
                State='ENABLED'
            )
            print(response['RuleArn'])
        except:
            pass

        print(e.response['Error']['Message'])
        res = {"status": "err", "msg": "could not calculate cart"}
    else:
        items = response['Responses']
        for item in items[table]:
            total = total + (item["price"] * cart[item["itemId"]])
        res = {"status": "ok", "total": float(total)}

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }

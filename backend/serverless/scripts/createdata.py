import boto3
import json
try:
    dynamodb = boto3.client('dynamodb')

    # aws dynamodb batch-write-item --request-items file://backend/serverless/scripts/create-orders-data.json
    with open("backend/serverless/scripts/create-orders-data.json") as f:
        data = f.read()
    try:
        orders = json.loads(data)
    except:
        orders = data


    response = dynamodb.batch_write_item(RequestItems=orders)
    try:
        f.close()
    except:
        pass


    # aws dynamodb batch-write-item --request-items file://backend/serverless/scripts/create-inventory-data.json
    with open("backend/serverless/scripts/create-inventory-data.json") as f:
        data = json.loads(f.read())
    try:
        inventory = json.loads(data)
    except:
        inventory = data

    response = dynamodb.batch_write_item(RequestItems=inventory)
    try:
        f.close()
    except:
        pass


    #  after:deploy:finalize: aws cognito-idp add-custom-attributes --user-pool-id us-east-1_dn9qLGOJ5 --custom-attributes Name=is_admin,AttributeDataType=String,Mutable=true
    with open("client/src/be-stack.json") as f:
        data = f.read()
    try:
        stack = json.loads(data)
    except:
        stack = data

    cognito = boto3.client('cognito-idp')
    response = cognito.add_custom_attributes(
        UserPoolId=stack["UserPoolId"],
        CustomAttributes=[
            {
                'Name': 'is_admin',
                'AttributeDataType': 'String',
                'Mutable': True,
            },
        ]
    )
    try:
        f.close()
    except:
        pass
except:
    pass

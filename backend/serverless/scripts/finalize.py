import sys
import os
import boto3
import uuid
import time
import json

def main():
    
    for i in range(0,len(sys.argv)):
        region, profile = None, None
        account = ""
        if sys.argv[i] == "--profile":
            profile = sys.argv[i+1]
            account = account + " --profile " + profile
        if sys.argv[i] == "--region":
            region = sys.argv[i+1]
            account = account + " --region " + region

    session = boto3.session.Session(region_name=region, profile_name=profile)

    print("- Filling Inventory database... ", end="")
    with open ("backend/serverless/scripts/create-inventory-data.json", "r") as f:
        inventory = json.loads(f.read())
    ddb = session.client('dynamodb')
    res = ddb.batch_write_item(RequestItems=inventory)
    print("[OK]")

    print("- creating admin default user:")
    print("-- creating admin default user... ", end="")
    cidp = session.client('cognito-idp')
    pool_id = None
    list_pools = cidp.list_user_pools(MaxResults=10)
    if "UserPools" in list_pools:
        for pool in list_pools["UserPools"]:
            if pool["Name"] == "dvsa-user-pool":
                pool_id = pool["Id"]
    
    if pool_id:
        print("[OK]")
        print("-- getting aws account-id... ", end="")
        TMP_PW = "changeme"
        sts = session.client('sts')
        res = sts.get_caller_identity()
        account_id = res.get("Account", None)
        if account_id:
            print("[OK]")
            print("-- creating cognito-idp user... ", end="")
            admin = "dvsa.admin@1secmail.com"
            userid = None
            try:
                response = cidp.admin_create_user(
                    UserPoolId=pool_id,
                    Username=admin,
                    UserAttributes=[
                        {
                            "Name": "email_verified",
                            "Value": "true"
                        },
                        {
                            "Name": "phone_number_verified",
                            "Value": "false"
                        },
                        {
                            "Name": "phone_number",
                            "Value": "+1123123123"
                        },
                        {
                            "Name": "email",
                            "Value": admin
                        },
                        {
                            "Name": "custom:is_admin",
                            "Value": "true"
                        }
                        
                    ],

                    TemporaryPassword=TMP_PW,
                    ForceAliasCreation=False,
                    MessageAction='SUPPRESS',
                    DesiredDeliveryMediums=[
                        'EMAIL',
                    ]
                )
                userid = response.get("User", {}).get("Username")
            except Exception as e:
                if str(e).find("UsernameExistsException") > -1:
                    res = cidp.list_users(UserPoolId=pool_id)
                    users = res.get("Users", [])
                    for user in users:
                        for att in user.get("Attributes", []):
                            if att["Name"] == "email" and att["Value"] == admin:
                                userid = user["Username"]
                                break
                
            DB = "DVSA-USERS-DB"
            if userid:
                print("[OK]")
                print("-- updating user in database... ", end="")
                dynamodb = session.client('dynamodb')
                response = dynamodb.put_item(
                    TableName=DB,
                    Item={
                        "address": {
                            "S": " "
                        },
                        "avatar": {
                            "S": "https://i.imgur.com/p3R1bCC.png
                        },
                        "created": {
                            "N": str(int(time.time()))
                        },
                        "email": {
                            "S": admin
                        },
                        "fullname": {
                            "S": "DVSA Administrator"
                        },
                        "isAdmin": {
                            "BOOL": True
                        },
                        "phone": {
                            "S": "+1123456789"
                        },
                        "status": {
                            "S": "CONFIRMED"
                        },
                        "userId": {
                            "S": userid
                        }
                    }
                )
    
                print("[OK]")
                print("Creating email address for... ", end="")
                invokeLambda = boto3.client('lambda')
                payload = {"action": "verify", "user": userid }
                res = invokeLambda.invoke(FunctionName='DVSA-USER-INBOX', InvocationType='Event', Payload=json.dumps(payload))
                print("[OK]")
                print("***************************************************************\n* admin user: [{}], password: [{}] *\n***************************************************************".format(admin, TMP_PW))

if __name__ == "__main__":
    main()

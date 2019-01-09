import json
import time
import boto3
import os

'''
# DEMO EVENT
{
  "userName": "<UUID>",
  "version": "1",
  "userPoolId": "xxxxxx",
  "callerContext": {
    "awsSdkVersion": "xxxxxxxxx",
    "clientId": "xxxxxxxxxxxxx"
  },
  "region": "<AWS_REGION>",
  "request": {
    "userAttributes": {
      "phone_number": "+1123123123123",
      "sub": "<UUID, same as userName>",
      "phone_number_verified": "false",
      "cognito:email_alias": "<EMAIL>",
      "cognito:user_status": "CONFIRMED",
      "email_verified": "true",
      "email": "<EMAIL, smae as above>"
    }
  },
  "response": {},
  "triggerSource": "PostConfirmation_ConfirmSignUp"
}
'''

def lambda_handler(event, context):
    userId = event["userName"]
    email = event["request"]["userAttributes"]["cognito:email_alias"]
    phone = event["request"]["userAttributes"]["phone_number"]
    status = event["request"]["userAttributes"]["cognito:user_status"]
    ts = int(time.time())
    if "Admin" in event["request"]["userAttributes"] and event["request"]["userAttributes"]["Admin"] == True:
      isAdmin = True
    else:
      isAdmin = False

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table( os.environ["USERS_TABLE"] )
    response = table.put_item(
       Item={
            'userId': userId,
            'email': email,
            'phone': phone,
            'address': " ",
            'status': status,
            'created': ts,
            'fullname': " ",
            'avatar': os.environ["GENERIC_AVATAR"],
            'isAdmin': isAdmin
        }
    )

    invokeLambda = boto3.client('lambda')
    payload = {"action": "verify", "user": userId }
    invokeLambda.invoke(FunctionName='DVSA-USER-INBOX', InvocationType='Event', Payload=json.dumps(payload))

    return event

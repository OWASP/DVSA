import json
import time
import boto3
import os


def lambda_handler(event, context):
  is_admin = False
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

  ses = boto3.client('ses')
  try:
    response = ses.verify_email_identity(
      EmailAddress = email
    )
  except:
    pass

  invokeLambda = boto3.client('lambda')
  payload = {"action": "verify", "user": userId }
  res = invokeLambda.invoke(FunctionName='DVSA-USER-INBOX', InvocationType='Event', Payload=json.dumps(payload))

  return event

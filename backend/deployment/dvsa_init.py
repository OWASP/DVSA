import boto3
import json
import decimal
import os
import re
from time import sleep, time
import urllib3
import logging

SUCCESS = "SUCCESS"
FAILED = "FAILED"
INVENTORY_FILE = "inventory.db"

HTTP = urllib3.PoolManager()
s3 = boto3.resource('s3')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
  print(json.dumps(event))
  cf_obj = to_cf_obj(event, context)
  curl_cmd = "curl -XPOST {} -H'Content-Type: application/json' --data '{}'".format(cf_obj["url"], cf_obj["data"])
  logger.debug("ONLY IF FAILED, use this cmd to finialize the deploytment: {}".format(curl_cmd))
  userid = None

  try:

    # create stack
    if event['RequestType'] != 'Delete':
      print("FINALIZING STACK CREATE")
      try:
        createWebsite()
      except:
        logger.exception("[INIT-ERROR-CREATE-WEBSITE]")
        return

      try:
        populateInvetory()
      except:
        logger.exception("[INIT-ERROR-INVENTORY]")

      try:
        userid = createAdminUser()
      except:
        logger.exception("[INIT-ERROR-ADMIN]")

      try:
        senders = ["dvsa.noreply@1secmail.com", os.environ.get("ADMIN_EMAIL", "dvsa.admin@1secmail.com")]
        senders.append("dvsa.{}.{}@1secmail.com".format(os.environ["ACCOUNT_ID"], ''.join(userid.split('-')))) if userid is not None else None        
        verifySESIdentities(senders)
      except:
        logger.exception("[INIT-ERROR-SES]")

    #  stack
    else:
      logger.debug("PREPARING STACK DELETE")
      buckets = [os.environ["CLIENT_BUCKET"], os.environ["RECEIPTS_BUCKET"], os.environ["FEEDBACK_BUCKET"]]
      for b in buckets:
        logger.debug("Empyting bucket: {}".format(b))
        try:
          bucket = s3.Bucket(b)
          bucket.objects.all().delete()
          bucket.object_versions.delete()
        except:
          logger.exception("[INIT-ERROR-EMPTY-S3]")

      try:
        removeSESIdentities()
      except:
        logger.exception("[INIT-ERROR-DELETE-SES]")
      
      for b in buckets:
        logger.debug("Deleting bucket: {}".format(b))
        try:
          bucket = s3.Bucket(b)
          bucket.delete()
        except:
          logger.exception("[INIT-ERROR-DELETE-S3]")
          continue
      
      try:
        deleteLogGroup()
      except:
        logger.exception("[INIT-ERROR-DELETE-LOGS]")

      try:
        lclient = boto3.client('lambda')
        logger.debug("Deleting myself...")
        lclient.delete_function(FunctionName=context.function_name)
      except:
        logger.exception("[INIT-ERROR-DELETE-LAMBDA]")
        
    response = SUCCESS

  except:
    logger.exception("[INIT-ERROR-FINAL]")
    response = FAILED

  HTTP.request("PUT", cf_obj["url"], body=cf_obj["data"], headers=cf_obj["headers"])
  return response


# generate website files with current configuration
def createWebsite():
  with open('dist_s3/bundle.js') as f:
    FileText = f.read()
  FileText = re.sub("<UserPoolClientId>", os.environ["USER_POOL_CLIENT_ID"], FileText)
  FileText = re.sub("<UserPoolId>", os.environ["USER_POOL_ID"], FileText)
  FileText = re.sub("<IdentityPoolId>", os.environ["IDENTITY_POOL"], FileText)
  FileText = re.sub("<ServiceEndpoint>", os.environ["ORDER_API"], FileText)
  FileText = re.sub("<ServerlessDeploymentBucketName>", os.environ["CLIENT_BUCKET"], FileText)

  with open('/tmp/bundle.js', "w") as f:
    f.write(FileText)

  bucket = s3.Bucket(os.environ["CLIENT_BUCKET"])
  bucket.objects.all().delete()
  s3.meta.client.upload_file('/tmp/bundle.js', os.environ["CLIENT_BUCKET"], 'bundle.js', ExtraArgs={'ContentType': "application/javascript"})
  s3.meta.client.upload_file('dist_s3/styles.css', os.environ["CLIENT_BUCKET"], 'styles.css', ExtraArgs={'ContentType': "text/css"})
  s3.meta.client.upload_file('dist_s3/index.html', os.environ["CLIENT_BUCKET"], 'index.html', ExtraArgs={'ContentType': "text/html; charset=utf-8"})
  # Upload images folder
  for root, dirs, files in os.walk('dist_s3/images'):
    for file in files:
      s3.meta.client.upload_file('dist_s3/images/'+file, os.environ["CLIENT_BUCKET"], 'images/'+file)
  logger.debug("bundle.js was replaced")


# send response to cloudformation
def to_cf_obj(event, context):
  cf_obj = {}
  cf_obj["url"] = event['ResponseURL']
  responseBody = {}
  responseBody['Status'] = "SUCCESS"
  responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
  responseBody['PhysicalResourceId'] = event.get("PhysicalResourceId", context.log_stream_name)
  responseBody['StackId'] = event.get('StackId')
  responseBody['RequestId'] = event.get('RequestId')
  responseBody['LogicalResourceId'] = event.get('LogicalResourceId')
  responseBody['Data'] = {}
  cf_obj["data"] = json.dumps(responseBody)
  cf_obj["headers"] = {
    'content-type': '',
    'content-length': str(len(cf_obj["data"]))
  }
  return cf_obj


# delete DVSA CloudWatch LogGroups
def deleteLogGroup():
  cwl = boto3.client('logs')
  res = cwl.describe_log_groups()
  lgs = res.get("logGroups", [])
  for lg in lgs:
    lg_name = lg.get("logGroupName", "X") 
    if lg_name.startswith("/aws/lambda/DVSA-"):
      cwl.delete_log_group(logGroupName=lg_name)
      logger.debug("Deleted LogGroup: {}".format(lg_name))
  return


# add inventory items and fake orders
def populateInvetory():
  print("uploading inventory file")
  if os.path.exists(INVENTORY_FILE):
    print|("found inventory file")
    s3.meta.client.upload_file('inventory.db', os.environ["CLIENT_BUCKET"], 'admin/inventory.db', ExtraArgs={'ContentType': "application/octet-stream"})
  else:
    print("could not find inventory file. Everything is ok! skipping...")

  dynamodb = boto3.client('dynamodb')
  print("writing orders to db")
  with open("create-orders-data.json") as json_file:
    items = json.load(json_file, parse_float=decimal.Decimal)
    res = dynamodb.batch_write_item(
      RequestItems=items
    )
    print(res)
  return


# verify dvsa.noreply@1secmail.com for sending receipts to uses
def verifySESIdentities(emails):
  ses = boto3.client('ses')
  logger.debug("verifying: {}".format(','.join(emails)))
  for email in emails:
    try:
        response = ses.verify_email_identity(
          EmailAddress=email
        )
        logger.debug("sent verify-email to: {}".format(email))
        if email.endswith("1secmail.com"):
          logger.debug("trying to auto-verify: {}".format(email))
          sleep(6)
          url = "https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}".format(email.split("@")[0], email.split("@")[1])
          req = HTTP.request("GET", url)

          if req.status < 300:
            msg_list = json.loads(req.data)
            aws_msg_list = []
            for msg in msg_list:
              if msg["subject"].find("Email Address Verification") > -1:
                aws_msg_list.append(msg["id"])
            
            if len(aws_msg_list) > 0:
              _id = max(aws_msg_list)
              url = "https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}".format(email.split("@")[0], email.split("@")[1], _id)
              req = HTTP.request("GET", url)

              if req.status < 300:              
                body = json.loads(req.data)["body"]
                startpoint=body.find("https://email-verification")
                endpoint = body.find("Your request will not be processed unless you confirm the address using this URL.")
                
                if (startpoint != -1 and endpoint != -1):
                  verification_link = body[startpoint:endpoint-2]
                  req = HTTP.request("GET", verification_link)
                  logger.debug("{}: Auto-verified!".format(email))

    except:
      logger.exception("[INIT-ERROR]")

    continue
  return


# remove DVSA-based SES identities
def removeSESIdentities():
  ses = boto3.client('ses')
  identities = ses.list_identities(
    IdentityType='EmailAddress'
  )
  for email in identities.get("Identities", []):
    if email.startswith("dvsa."):
      ses._identity(
        Identity=email
      )
  return


#create admin user with provided email address
def createAdminUser():
  cidp = boto3.client('cognito-idp')
  pool_id = os.environ["USER_POOL_ID"]
  TMP_PW = "changeme!"
  userid = None
  admin_email = os.environ.get("ADMIN_EMAIL", "dvsa.admin@1secmail.com")
  logger.debug("creating admin user for: {}".format(admin_email))
  try:
    response = cidp.admin_create_user(
      UserPoolId=pool_id,
      Username=admin_email,
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
              "Value": admin_email
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
    logger.debug(response)
    userid = response.get("User", {}).get("Username")

  except Exception as e:
    if str(e).find("UsernameExistsException") > -1:
      logger.debug("User already exists, looking for userid")
      res = cidp.list_users(UserPoolId=pool_id)
      users = res.get("Users", [])
      for user in users:
        for att in user.get("Attributes", []):
          if att["Name"] == "email" and att["Value"] == admin:
            userid = user["Username"]
            logger.debug("found userid: {}".format(userid))
            break
    else:
      logger.exception("[INIT-ERROR]")
      return

  logger.debug("admin in Cognito")
  DB = "DVSA-USERS-DB"
  try:
    if userid:
      dynamodb = boto3.client('dynamodb')
      response = dynamodb.put_item(
        TableName=DB,
        Item={
          "address": {
              "S": " "
          },
          "avatar": {
              "S": "https://i.imgur.com/TbXpDM4.png"
          },
          "created": {
              "N": str(int(time()))
          },
          "email": {
              "S": admin_email
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
    logger.debug(response)
  except:
    logger.exception("[INIT-ERROR]")

  logger.debug("admin added to dynamodb")
  return userid

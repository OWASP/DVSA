import logging
import boto3
import json
import decimal
import os
import re
import time
from botocore.vendored import requests

log = logging.getLogger()
log.setLevel(logging.INFO)

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def lambda_handler(event, context):
    print("event------------- ", event)
    try:
        if event['RequestType'] != 'Delete':
            with open('dist_s3/bundle.js') as f:
                FileText = f.read()
                FileText = re.sub("<USER_POOL_CLIENT_ID_TAG>", os.environ["USER_POOL_CLIENT_ID"], FileText)
                FileText = re.sub("<USER_POOL_ID_TAG>", os.environ["USER_POOL_ID"], FileText)
                FileText = re.sub("<IDENTITY_POOL_ID_TAG>", os.environ["IDENTITY_POOL"], FileText)
                FileText = re.sub("<SERVICE_ENDPOINT_TAG>", os.environ["ORDER_API"], FileText)
                FileText = re.sub("<DEP_BUCKET_NAME_TAG>", os.environ["CLIENT_BUCKET"], FileText)

                with open('/tmp/bundle.js', "w") as f:
                    f.write(FileText)

            print("Emptying bucket---")
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(os.environ["CLIENT_BUCKET"])
            bucket.objects.all().delete()
            print("Empty bucket complete---")
            print("Uploading dist folder to s3---")

            s3.meta.client.upload_file('/tmp/bundle.js', os.environ["CLIENT_BUCKET"], 'bundle.js', ExtraArgs={'ContentType': "application/javascript"})
            s3.meta.client.upload_file('dist_s3/styles.css', os.environ["CLIENT_BUCKET"], 'styles.css', ExtraArgs={'ContentType': "text/css"})
            s3.meta.client.upload_file('dist_s3/index.html', os.environ["CLIENT_BUCKET"], 'index.html', ExtraArgs={'ContentType': "text/html; charset=utf-8"})
            # Upload images folder
            for root, dirs, files in os.walk('dist_s3/images'):
                for file in files:
                    s3.meta.client.upload_file('dist_s3/images/'+file, os.environ["CLIENT_BUCKET"], 'images/'+file)
            print("Uploading dist folder complete---")
            try:
                populateDB("init")
            except Exception as e:
                print(str(e))
                pass
            try:
                handleSes("init")
            except Exception as e:
                print(str(e))
                pass

        else:
            print("Emptying buckets...")
            print("Emptying client bucket before deleting stack---")
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(os.environ["CLIENT_BUCKET"])
            bucket.objects.all().delete()
            print("Emptying bucket complete!")
            print("deleting bucket---")
            bucket.delete()
            print("Emptying receipts bucket before deleting stack---")
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(os.environ["RECEIPTS_BUCKET"])
            bucket.objects.all().delete()
            print("Emptying bucket complete!")
            print("deleting bucket---")
            bucket.delete()
            print("Emptying feedback bucket before deleting stack---")
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(os.environ["FEEDBACK_BUCKET"])
            bucket.objects.all().delete()
            print("Emptying bucket complete!")
            print("deleting bucket---")
            bucket.delete()
            try:
                populateDB("delete")
            except Exception as e:
                print(str(e))
                pass
            try:
                handleSes("delete")
            except Exception as e:
                print(str(e))
                pass
            try:
                deleteLogGroup()
            except Exception as e:
                print(str(e))
                pass

    except Exception as e:
        print(str(e))
        pass

    response = send(event, context, SUCCESS, {}, None)
    return {
        "Response": response
    }


def send(event, context, responseStatus, responseData, physicalResourceId):
    responseUrl = event['ResponseURL']
    log.info("Event: " + str(event))
    log.info("ResponseURL: " + responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    log.info("Response body: " + str(json_responseBody))

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        log.info("Status code: " + str(response.reason))
        return SUCCESS

    except Exception as e:
        log.error("send(..) failed executing requests.put(..): " + str(e))
        return FAILED


def deleteLogGroup():
    cwl = boto3.client('logs')
    response = cwl.delete_log_group(
        logGroupName='/aws/lambda/DVSA-INIT'
    )


def handleSes(action):
    sender = "dvsa.noreply@mailsac.com"
    if action == "delete":
        removeIdentities()
    else:
        verifySes(sender)


def populateDB(action):
    if action == "delete":
        pass
    else:
        populateInvetory()


# add inventory items from inventory_data.json
def populateInvetory():
    dynamodb = boto3.client('dynamodb')

    with open("create-inventory-data.json") as json_file:
        items = json.load(json_file, parse_float=decimal.Decimal)
        response = dynamodb.batch_write_item(
            RequestItems=items
        )

    with open("create-orders-data.json") as json_file:
        items = json.load(json_file, parse_float=decimal.Decimal)
        response = dynamodb.batch_write_item(
            RequestItems=items
        )


# verify dvsa.noreply@mailsac.com for sending receipts to uses
def verifySes(email):
    ses = boto3.client('ses')
    response = ses.verify_email_identity(
        EmailAddress=email
    )
    time.sleep(6)
    print("Getting emails for address...")
    try:
        res = requests.get("https://mailsac.com/api/addresses/" + email + "/messages")
    except Exception as e:
        err = "[ERR] "
        print(err + (str(e)))
        return False

    if res.status_code != 200:
        return False

    j = json.loads(res.text)
    _id = j[len(j) - 1]["_id"]
    print("Getting verification link...")
    try:
        res = requests.get("https://mailsac.com/api/text/" + email + "/" + _id)
    except Exception as e:
        err = "[ERR] "
        print(err + (str(e)))
        return False

    if res.status_code != 200:
        return False

    body = res.text
    startpoint = body.find("https://email-verification")
    endpoint = body.find("Your request will not be processed unless you confirm the address using this URL.")

    if startpoint == -1 or endpoint == -1:
        return False

    verification_link = body[startpoint:endpoint - 2]
    try:
        res = requests.get(verification_link)
    except Exception as e:
        err = "[ERR] "
        print(err + (str(e)))
        return False

    if (("Location" in res.headers and res.headers["Location"].find("ses/verifysuccess") == -1) and res.text.find(
            "You have successfully verified an email address") != -1):
        return False

    print("Email verified successfully!")
    print("Deleting email tail...")
    try:
        res = requests.delete("https://mailsac.com/api/addresses/" + email + "/messages/" + _id)
    except Exception as e:
        err = "[ERR] "
        print(err + (str(e)))
        return False

    if res.status_code != 200:
        return False

    print("Email deleted.")
    return True


# remove all dvsa-created email addresses (dvsa.<XXX>@mailsac.com)
def removeIdentities():
    ses = boto3.client('ses')
    print("Getting SES identities..."),
    identities = ses.list_identities(
        IdentityType='EmailAddress'
    )
    print(" [OK]")
    for email in identities["Idetities"]:
        if email.startswith("dvsa.") and email.endswith("@mailsac.com"):
            print("Deleting SES identity: " + email),
            ses.delete_identity(
                Identity=email
            )
            print(" [OK]")

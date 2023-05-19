import json
import boto3
import urllib.parse
import os
import datetime
import decimal


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

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    key = urllib.parse.unquote_plus(urllib.parse.unquote(key))
    order = key.split("/")[3]
    orderId = order.split("_")[0]
    userId = order.split("_")[1].replace(".raw", "")

    s3 = boto3.client('s3')
    # download file to /tmp
    download_path = '/tmp/' + order.replace(".raw", ".txt")

    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    os.system('echo -e "\t----------------------\n\t\tDate: {}" >> {}'.format(date, download_path))

    # print download_path
    try:
        s3.download_file(bucket, key, download_path)

        # delete original file
        #s3.delete_object(Bucket=bucket, Key=key)
        # upload new file (txt)
        s3.upload_file(download_path, bucket, key.replace(".raw", ".txt"))

        # get signed url
        signed_link = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key.replace(".raw", ".txt")},
                                                ExpiresIn=259200)
    except Exception as e:
        print(e)
    # GET ITEMS FOR ORDER
    dynamodb = boto3.resource('dynamodb')
    order_table = dynamodb.Table(os.environ["ORDERS_TABLE"])
    response = order_table.get_item(
        Key={
            "orderId": orderId,
            "userId": userId
        }
    )

    if 'Item' not in response:
        res = {"status": "err", "msg": "could not find order"}
    else:
        status = int(json.dumps(response["Item"]['orderStatus'], cls=DecimalEncoder))
        if status != 200:
            res = {"status": "err", "msg": "invalid order status"}
        else:
            token = response["Item"]['confirmationToken']
            name = response["Item"]["address"]["name"]
            address = response["Item"]["address"]["address"]
            email_addr = response["Item"]["address"]["email"]

            sts = boto3.client("sts")
            account_id = sts.get_caller_identity()["Account"]
            secmail = "dvsa.{}.{}@1secmail.com".format(account_id, ''.join(userId.split('-')))

            # create email
            subject = 'Your DVSA Order: Confirmed'.format(token)
            email_msg = \
                '''
                Dear {}, <br><br>

                Your order: <b>{}</b> has been <b>confirmed</b> and will be sent to: <br>

                {}

                <br><br>Please, download receipt from the <a href="{}">this link</a>.<br><br>

                Best,<br>
                DVSA Team
                <br>
                <a href="https://www.owasp.org/index.php/OWASP_DVSA"><img src="https://i.imgur.com/P3fU4GH.png" width="200px" height="75px"/></a>

                '''.format(name, token, address, signed_link)

            # SEND EMAIL TO CUSTOMER

            ses = boto3.client('ses')
            destinations = [secmail, email_addr]
            for address in destinations:
              try:
                  response = ses.send_email(
                      Destination={
                          'ToAddresses': [address]
                      },
                      Message={
                          'Body': {
                              'Html': {
                                  'Charset': 'UTF-8',
                                  'Data': email_msg
                              },
                          },
                          'Subject': {
                              'Charset': 'UTF-8',
                              'Data': subject,
                          },
                      },
                      Source=os.environ["SOURCE_EMAIL"],
                  )
                  print("Sent email to: {}".format(address))
              except Exception as e:
                print("could not send email to: {}".format(address))
                print(str(e))
              

            res = {"status": "ok", "msg": "receipt email sent"}

    return res

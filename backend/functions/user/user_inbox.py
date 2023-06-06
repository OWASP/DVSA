import json
import time
import boto3
import urllib3
import base64

HTTP = urllib3.PoolManager()


def getEmailList(email):
    try:
        url = "https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}".format(email.split("@")[0], email.split("@")[1])
        res = HTTP.request("GET", url)
    except Exception as e:
        err = "[ERR] "
        print(err + (str(e)))

    if res.status != 200:
        return False
 
    data = res.data
    return json.loads(data)


def getEmailById(email, _id, mod):
    try:
        url = "https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}".format(email.split("@")[0], email.split("@")[1], _id)
        res = HTTP.request("GET", url)
    except Exception as e:
        err = "[ERR] "
        print(err + str(e))
        return False

    if res.status == 200:
        data = json.loads(res.data)
        return data[mod] if len(data[mod]) > 0 else data["body"]
          
    return False


def deleteMailbox(email):
  url = "https://www.1secmail.com/mailbox"
  data = "action=deleteMailbox&domain={}&login={}".format(email.split("@")[1], email.split("@")[0])
  headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
  res = HTTP.request("POST", url, body=data, headers=headers)
  if res.status == 200:
    return True
  return False


def lambda_handler(event, context):
    action = event["action"]
    userId = event["user"]

    sts = boto3.client("sts")
    account_id = sts.get_caller_identity()["Account"]
    secmail = "dvsa.{}.{}@1secmail.com".format(account_id, ''.join(userId.split('-')))
    #print("MAIL", secmail)

    if action == "delete":
      return {"status": "ok", "msg": "mailbox cleared"} if deleteMailbox(secmail) else {"status": "err", "msg": "could not delete mailbox"}


    if action == "get":
        _id = event["msgId"]
        mod = 'htmlBody' if event["type"] == 'html' else 'textBody'
        body = getEmailById(secmail, _id, mod)
        if body:
            data = base64.b64encode(body.encode())
            res = {"status": "ok", "message": data.decode("utf-8")}
            return res

        else:
            res = {"status": "err", "msg": "could not retrieve email"}
            return res

    # if action == "delete":
    #     _id = event["msgId"]
    #     if (deleteEmail(secmail, _id)):
    #         res = {"status": "ok", "msg": "message deleted"}
    #     else:
    #         res = {"status": "err", "msg": "could not delete message"}

    #     return res

    if action == "inbox":
        messages = []
        emails = getEmailList(secmail)
        if not emails and not isinstance(emails, list):
            res = {"status": "err", "msg": "could not retrieve emails for: " + secmail}
            return res

        for email in emails:
            sender = email["from"]
            if sender == "dvsa.noreply@1secmail.com" or sender.endswith("amazonses.com"):
                item = {"date": email["date"], "msg-id": email["id"], "subject": email["subject"],
                        "sender": sender}
                messages.append(item)

        res = {"status": "ok", "messages": messages}
        return res

    elif action == "verify":
        ses = boto3.client('ses')
        ses.verify_email_identity(
            EmailAddress=secmail
        )
        time.sleep(2)
        
        try:
            req = HTTP.request("GET", "https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}".format(secmail.split("@")[0], secmail.split("@")[1]))
        except Exception as e:
            res = {"status": "err", "msg": str(e)}
            print(json.dumps(res))
            return res
            
        if req.status != 200:
            res = {"status": "err", "msg": "got status code: " + str(req.status)}
            return res
            
        msg_list = json.loads(req.data)
        aws_msg_list = []
        for msg in msg_list:
            if msg["subject"].find("Email Address Verification") > -1:
                aws_msg_list.append(msg["id"])

        if not aws_msg_list:
            res = {"status": "err", "msg": "Could not get verification link"}
            return res
            
        try:
            req = HTTP.request("GET", "https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}".format(secmail.split("@")[0], secmail.split("@")[1], max(aws_msg_list)))
        except Exception as e:
            res = {"status": "err", "msg": str(e)}
            print(res)
            return res
        
        if req.status != 200:
            res = {"status": "err", "msg": "got status code: " + str(req.status)}
            
        email_data = json.loads(req.data)
        body = email_data["body"]
        startpoint = body.find("https://email-verification")
        endpoint = body.find("Your request will not be processed unless you confirm the address using this URL.")
        
        if (startpoint == -1 or endpoint == -1):
            res = {"status": "err", "msg": "Could not find verification link in body."}
            print(res)
            return res
        
        verification_link = body[startpoint:endpoint-2]
        try:
            req = HTTP.request("GET", verification_link)
        except Exception as e:
            res = {"status": "err", "msg": str(e)}
            print(res)
            return res
            
        if req.status != 200:
            res = {"status": "err", "msg": "got status code: " + str(req.status)}
            
        data = req.data.decode('utf-8')
        if data.find("You have successfully verified an email address") > -1 :
            res = {"status": "ok", "msg": str(secmail) + " was verified"}
            print(res)
            return res

        else:
            res = {"status": "err", "msg": "Could not verify email"}
            print(res)
            return res

        res = {"status": "ok", "msg": str(secmail) + " was verified"}
        print(req.data)
        return res

    else:
        return "Unkown action" + action

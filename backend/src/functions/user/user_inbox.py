import json
import time
import boto3
import urllib
import urllib2
import base64



def getEmailList(email):
    try:
        res = urllib.urlopen("https://mailsac.com/api/addresses/" + email + "/messages")
    except Exception as e:
        err = "[ERR] "
        print(err + (str(e)))

    if res.getcode() != 200:
        return False
    else:
        return res.read()


def getVerificationEmailId(email):
    i=0
    while i<5:
        data = getEmailList(email)
        if len(data) < 10:
            i = i + 1
            time.sleep(1)
        else:
            j = json.loads(data)
            break

    if len(data) == 0:
        return 99

    id = j[len(j) - 1]["_id"]
    return id


def getEmailById(email, _id, mod):
    try:
        res = urllib.urlopen("https://mailsac.com/api/{}/{}/{}".format(mod, email, _id))
    except Exception as e:
        err = "[ERR] "
        print (err + (str(e)))
        return False

    if res.getcode() != 200:
        return False

    else:
        return res.read()


def getVerificationLink(email, _id):
    body = getEmailById(email, _id, "text")
    startpoint = body.find("https://email-verification")
    endpoint = body.find("Your request will not be processed unless you confirm the address using this URL.")
    if (startpoint == -1 or endpoint == -1):
        return False

    verificationlink = body[startpoint:endpoint - 2]
    return verificationlink


def verifyEmail(link):
    try:
        res = urllib.urlopen(link)
    except Exception as e:
        err = "[ERR] "
        print (err + (str(e)))

    if (("Location" in res.headers and res.headers["Location"].find("ses/verifysuccess") == -1) and res.read().find(
            "You have successfully verified an email address") != -1):
        return False

    return {"status": "ok", "msg": "email verified"}


def deleteEmail(email, _id):
    try:
        uri = ("https://mailsac.com/api/addresses/" + email + "/messages/" + _id)
        request = urllib2.Request(uri)
        request.get_method = lambda: 'DELETE'
        res = urllib2.urlopen(request)

    except Exception as e:
        err = "[ERR] "
        print (err + (str(e)))
        return False

    if res.getcode() != 200:
        return False

    return True


def lambda_handler(event, context):
    action = event["action"]
    userId = event["user"]

    sts = boto3.client("sts")
    account_id = sts.get_caller_identity()["Account"]
    mailsac_email = "dvsa.{}.{}@mailsac.com".format(account_id, ''.join(userId.split('-')))
    print ("MAIL", mailsac_email)

    if action == "get":
        _id = event["msgId"]
        mod = event["type"]
        if mod == 'html':
            mod = 'dirty'
        body = getEmailById(mailsac_email, _id, mod).encode("UTF-8")
        if (body):
            data = base64.b64encode(body)
            res = {"status": "ok", "message": data}
            return res

        else:
            res = {"status": "err", "msg": "could not retrieve email"}
            return res

    if action == "delete":
        _id = event["msgId"]
        if (deleteEmail(mailsac_email, _id)):
            res = {"status": "ok", "msg": "message deleted"}
        else:
            res = {"status": "err", "msg": "could not delete message"}

        return res


    if action == "inbox":
        messages = []
        emails = getEmailList(mailsac_email)
        if not emails:
            res = {"status": "err", "msg": "could not retrieve emails for: " + mailsac_email}
            return res

        list = json.loads(emails)
        for email in list:
            sender = email["from"][0]["address"]
            if (sender == "dvsa.noreply@mailsac.com"):
                item = {"date": email["received"], "msg-id": email["_id"], "subject": email["subject"], "sender": sender}
                messages.append (item)

        res = {"status": "ok", "messages": messages}
        return res


    else:
        ses = boto3.client('ses')
        response = ses.verify_email_identity(
            EmailAddress=mailsac_email
        )
        time.sleep(2)

        _id = getVerificationEmailId(mailsac_email)
        if not _id:
            res = {"status": "err", "msg": "Could not get messages from account"}
            print (res)
            return res

        elif id == 99:
            res = {"status": "err", "msg": "Something went wrong. Please try to login now."}
            print(res)
            return res

        link = getVerificationLink(mailsac_email, _id)
        if not link:
            res = {"status": "err", "msg": "Could not get verification link"}
            return res

        verified = verifyEmail(link)
        if not verified:
            res = {"status": "err", "msg": "Could not verify email"}
            print (res)
            return res

        deleted = deleteEmail(mailsac_email, _id)

        res = {"status": "ok", "msg": str(mailsac_email) + " was verified" }
        print(res)
        return res


import urllib3
import os
import json
import sys
import time

HTTP = urllib3.PoolManager()

def err():
  print ("[ERR] Could not verify email account.\n")
  print ("Make sure you've specified a region using \"aws configure\" and try again ($ python3 backend/serverless/scripts/verifysesaccount.py) or manualy verify email from: https://www.1secmail.com/?login=dvsa.noreply&domain=1secmail.com")
  return False

def getEmailId(email):
  latest_id = None
  try:
    req = HTTP.request("GET", "https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}".format(email.split("@")[0], email.split("@")[1]))
  except Exception as e:
    err = "[ERR] "
    print (err + (str(e)))
    return False
  
  if req.status > 299:
    return False
    
  msg_list = json.loads(req.data)
  aws_msg_list = []
  for msg in msg_list:
    if msg["subject"].find("Email Address Verification") > -1:
      aws_msg_list.append(msg["id"])
  
  return max(aws_msg_list) if len(aws_msg_list) > 0 else None


def getVerificationLink(email, _id):
  try:
    req = HTTP.request("GET", "https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}".format(email.split("@")[0], email.split("@")[1], _id))
  except Exception as e:
    err = "[ERR] "
    print (err + (str(e)))
    return False
  
  if req.status > 299:
    return False
    
  body = json.loads(req.data)["body"]
  startpoint=body.find("https://email-verification")
  endpoint = body.find("Your request will not be processed unless you confirm the address using this URL.")
  
  if (startpoint == -1 or endpoint == -1):
    return False
  return body[startpoint:endpoint-2]
  

def verifyEmail(link):
  try:
    req = HTTP.request("GET", link)
  except Exception as e:
    err = "[ERR] "
    print (err + (str(e)))
    return False
  data = req.data.decode("utf-8")
  if data.find("You have successfully verified an email address") > -1 :
    return True
  return False


def verify(email):
  print("- SES Email account verification for: {}".format(email))
  
  print("-- requesting account verification...", end="")
  os.system("aws ses verify-email-identity --email-address {}".format(email))
  time.sleep(3)
  print (" [OK]")
  
  print("-- verifying verification mail received...", end="")
  _id = getEmailId(email)
  if not _id:
    err()
    return False
  print (" [OK]")
  
  print("-- getting verification link...", end="")
  link = getVerificationLink(email, _id)
  if not link:
    err()
    return False
  print (" [OK]")

  print ("-- verifying email address...", end="")
  verified = verifyEmail(link)
  if not verified:
    err()
    return False
  print (" [OK]")
  
  
  return True

def removeIdentities():
  print ("Getting SES identities...", end="")
  os.system('aws ses list-identities > /tmp/dvsa')
  print (" [OK]")
  with open('/tmp/dvsa', 'r') as f:
    j = json.loads(f.read().rstrip())
    emails = j["Identities"]
    for email in emails:
      if email.startswith("dvsa.") and email.endswith("@1secmail.com"):
        print ("Deleting SES identity: " + email),
        os.system("aws ses delete-identity --identity {}".format(email))
        print(" [OK]")


def main():
  if sys.argv[1] == "--remove":
    removeIdentities()
  elif sys.argv[1] == "--verify":
    sender = "dvsa.noreply@1secmail.com"
    verify(sender)
  else:
    sys.exit("Invalid argument [--remove, --verify]. Check your serverless.yml file.")
    
if __name__ == "__main__":
  main()

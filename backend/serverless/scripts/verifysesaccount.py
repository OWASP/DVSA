import requests
import os
import json
import sys
import time

def err():
	print ("[ERR] Could not verify email account.\n")
	print ("Make sure you've specified a region using \"aws configure\" and try again ($python backend/serverless/scripts/verifysesaccount.py), or manually browse to: https://mailsac.com/inbox/noreply.dvsa@mailsac.com and approve the email account")
	return False

def getEmailList(email):
	try:
		res=requests.get("https://mailsac.com/api/addresses/" + email + "/messages")
	except Exception as e:
		err = "[ERR] "
		print (err + (str(e)))
		return False
	
	if res.status_code != 200:
		return False

	j = json.loads(res.text)
	messageCount = len(j)

	if not messageCount:
		return False

	id = j[messageCount-1]["_id"]
	return id

def getVerificationLink(email, _id):
	try:
		res=requests.get("https://mailsac.com/api/text/" + email + "/"+_id)
	except Exception as e:
		err = "[ERR] "
		print (err + (str(e)))
		return False
	
	if res.status_code != 200:
		return False
		
	body=res.text
	startpoint=body.find("https://email-verification")
	endpoint = body.find("Your request will not be processed unless you confirm the address using this URL.")
	
	if (startpoint == -1 or endpoint == -1):
		return False
	
	verificationlink = body[startpoint:endpoint-2]
	return verificationlink
	
def verifyEmail(link):
	try:
		res = requests.get(link)
	except Exception as e:
		err = "[ERR] "
		print (err + (str(e)))
		return False

	if ( ("Location" in res.headers and res.headers["Location"].find("ses/verifysuccess") == -1) and res.text.find("You have successfully verified an email address") != -1 ):
		return False
	
	return True
	
def deleteEmail(email, _id):
	try:
		res = requests.delete("https://mailsac.com/api/addresses/" + email + "/messages/" + _id)
	except Exception as e:
		err = "[ERR] "
		print (err + (str(e)))
		return False
	
	if res.status_code != 200:
		return False
	
	return True

def verify(email):
	print("SES Email account verification for: " + email)
	
	print("- requesting account verification..."),
	os.system("aws ses verify-email-identity --email-address " + email)
	time.sleep(3)
	print (" [OK]")  
	
	print("- verifying verification mail received..."),
	_id = getEmailList(email)
	if not _id:
		err()
		return False
	print (" [OK]")  
	
	print("- getting verification link..."),
	link = getVerificationLink(email, _id)
	if not link:
		err()
		return False
	print (" [OK]")

	print ("- verifying email address..."),
	verified = verifyEmail(link)
	if not verified:
		err()
		return False
	print (" [OK]")
	
	print ("- deleting email message..."),
	deleted = deleteEmail(email, _id)
	if not deleted:
		print ("[-] Could not delete email... (weird, but still [OK])")
	print (" [OK]")
	
	return True


def removeIdentities():
	print ("Getting SES identities..."),
	os.system('aws ses list-identities > /tmp/dvsa')
	print (" [OK]")
	with open('/tmp/dvsa', 'r') as f:
		j = json.loads(f.read().rstrip())
		emails = j["Identities"]
		for email in emails:
			if email.startswith("dvsa.") and email.endswith("@mailsac.com"):
				print ("Deleting SES identity: " + email),
				os.system("aws ses delete-identity --identity " + email)
				print(" [OK]")


def main():
	if sys.argv[1] == "--remove":
		removeIdentities()
	elif sys.argv[1] == "--verify":
		sender = "dvsa.noreply@mailsac.com"
		verify(sender)
	else:
		sys.exit("Invalid argument [--remove, --verify]. Check your serverless.yml file.")
		
if __name__ == "__main__":
	main()

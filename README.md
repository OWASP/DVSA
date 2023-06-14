
# ![alt OWASP DVSA](https://i.imgur.com/G15BF6m.png)

## a Damn Vulnerable Serverless Application

- - -
Damn Vulnerable Serverless Application (DVSA) is a deliberately vulnerable application aiming to be an aid for security professionals to test their skills and tools in a legal environment, help developers better understand the processes of securing serverless applications and to aid both students & teachers to learn about serverless application security in a controlled class room environment.

The aim of DVSA is to **practice some of the most common serverless vulnerabilities**, with a simple straightforward interface.

Please note, there are both **documented & undocumented vulnerabilities** with this software. This is intentional. You are encouraged to try and discover as many issues as possible.


- - -
## Disclaimer

***Do not install DVSA on a production account***

We do not take responsibility for the way in which any one uses this application (DVSA). We have made the purposes of the application clear and it should not be used maliciously. We have given warnings and taken measures to prevent users from installing DVSA on to production accounts.


- - -
## Deployment from [Application Repository](AWS/VIDEOS/reo_deploy.mp4)
- Deploy DVSA from the [AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:674087993380:applications~OWASP-DVSA)

- After deployment is complete. Click on 'View CloudFormation Stack'

- Under 'Outputs' you will find the URL for the application (DVSA Website URL)

- - - 

## Local Development & Deployment

### Client
##### Prerequisites for re-building client
- Node 8.16.2 ([switching between Node versions during dev](https://github.com/tj/n))
- python2 (needed for npm i node-gyp. You can using `npm config set python /path/to/your/python2`)

##### Build client
- `$ ./dvsa.sh client-build`

##### Update client file with previously deployed backend
- `$ ./dvsa.sh client-connect --stack <STACK_NAME>`

##### Updating deployed client with local changes
- `$ ./dvsa.sh client-update --stack/--bucket`
- `$ ./dvsa.sh client-update -h/--help` for more options

##### Run Client locally
- `$ ./dvsa.sh client-start`


![](https://i.imgur.com/ZfjEyiM.png)
### Backend

##### Prerequisites for building backend
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

##### Step-by-Step:
- Make desired changes to backend code under backend/functions
- Make desired changes to your cloudformation template.yml
- If you need post-deployment changes, you can add files to `backend/deployment/` and use the `backend/deployment/dvsa_init.py` function that runs at the end of the deployment to execute the required actions.
- `$ ./dvsa.sh package-template` (OPTIONAL: -h/--help for more options)
- Deploy the output template-file with Cloudformation console/cli

![](https://i.imgur.com/aeBKZav.png)

##### Run Backend locally
You can use [SAM Local](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html) to start [Lambda functions](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-start-lambda.html) and [APIs](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-start-api.html)

Alternatively, you can use [LocalStack](https://github.com/localstack/localstack)

**_Note_**: If you want to point your local client to your local backend, run `$ ./dvsa.sh client-connect` and REPLACE the endpoint of `ServiceEndpoint` with `http://localhost:3000` (It will still be using the Cognito pools in AWS).

![](https://i.imgur.com/ZfjEyiM.png)
#### Email subscription

DVSA sends receipts in the email. You can use the built-in **Inbox** page within the application to get the emails and obtain the receipts. Each user will be automatically assigned an email from `1secmail.com` which will be automatically verified. Real emails will be sent to their account and will appear in the application Inbox page.

If you want users to receive emails to their actual registered email account (e.g. gmail):
- Send an email verification link to the desired email address, by running the following command (after clicking on the received link, emails will **also** be sent to their actual email address):

`aws ses verify-email-identity --email-address <your_email>`

- [Request a sending limit increase](https://console.aws.amazon.com/support/v1#/case/create?issueType=service-limit-increase&limitType=service-code-ses). This will allow your entire cloud account to send emails to any address.

- - -
![](https://i.imgur.com/ZfjEyiM.png)
# Additional Info
## Presentation
[Download](CONTENT/OWASP_DC_SLS_Top10.pdf)



## Documentation

#### AWS ####

see [LESSONS](CONTENT/AWS/LESSONS/README.md) for information about hacking DVSA.

see [VIDEOS](CONTENT/AWS/VIDEOS) for how to deploy, use and hack DVSA.


- - -
## Links
[OWASP Top 10 - Serverless Interpretation](https://github.com/OWASP/Serverless-Top-10-Project/blob/master/README.md)

[Deep-Dive into Serverless Attacks - Series](https://www.protego.io/category/a-deep-dive-into-serverless-attacks/)

[OWASP Serverless Top 10 Project](https://www.owasp.org/index.php/OWASP_Serverless_Top_10_Project)

[Twitter account ](https://twitter.com/DVSAowasp) (hackable)

[Slack Channel #project-sls-top-10](https://owasp.slack.com/join/shared_invite/enQtNDI5MzgxMDQ2MTAwLTEyNzIzYWQ2NDZiMGIwNmJhYzYxZDJiNTM0ZmZiZmJlY2EwZmMwYjAyNmJjNzQxNzMyMWY4OTk3ZTQ0MzFhMDY)

[DVSA blog post](https://www.protego.io/level-up-on-security-with-the-new-damn-vulnerable-serverless-app/)

[**In the News**](news.md)


- - -
## Acknowledgements
DVSA was created by [Tal Melamed](https://github.com/4ppsec)


- - -
## License
Damn Vulnerable Serverless Application (DVSA) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Damn Vulnerable Serverless Application (DVSA) is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Damn Vulnerable Serverless Application (DVSA).  If not, see http://www.gnu.org/licenses/.

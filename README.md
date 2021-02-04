
# ![alt DVSA](https://i.imgur.com/Z4L7MqL.png)

## a Damn Vulnerable Serverless Application

- - -
Damn Vulnerable Serverless Application (DVSA) is a deliberately vulnerable application aiming to be an aid for security professionals to test their skills and tools in a legal environment, help developers better understand the processes of securing serverless applications and to aid both students & teachers to learn about serverless application security in a controlled class room environment.

The aim of DVSA is to **practice some of the most common serverless vulnerabilities**, with a simple straightforward interface.

Please note, there are **both documented and undocumented vulnerabilities** with this software. This is intentional. You are encouraged to try and discover as many issues as possible.




- - -
## Disclaimer

***Do not install DVSA on a production account***

We do not take responsibility for the way in which any one uses this application (DVSA). We have made the purposes of the application clear and it should not be used maliciously. We have given warnings and taken measures to prevent users from installing DVSA on to production accounts.


- - -
## Deployment

#### [Application Repository](AWS/VIDEOS/reo_deploy.mp4)
- Deploy DVSA from the [AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:889485553959:applications~DVSA)

- After deployment is complete. Click on 'View CloudFormation Stack'

- Under 'Outputs' you will find the URL for the application (DVSA Website URL)


![](https://i.imgur.com/ZfjEyiM.png)
#### [Serverless Framework](AWS/VIDEOS/serverless_deploy.mp4)

You must run serverless deploy commands with an environment variable profile (e.g. `AWS_PROFILE=<aws-profile-name>`) instead of the serverless argument.

##### Clone Project
- `git clone git@github.com:OWASP/DVSA.git`

##### Install nodejs==14.15.4 and npm (later versions break the lambda packaging: [issue](https://github.com/serverless/serverless/issues/8794))
- https://nodejs.org/download/release/latest-v14.x/
- https://www.npmjs.com/package/npm?activeTab=versions

##### Configure nodejs to use python2.7
- `npm config set python python2.7`

##### Install Serverless
- `npm install -g serverless`

##### Install AWS-CLI
- `pip install awscli --upgrade --user`

##### Install npm's python dependencies
- `pip install requests --user`

##### Verify AWS-CLI Installation
- `aws --version`

If you get a "command not found" error, see the "Steps to Take after Installation" section [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html#install-tool-pip).

##### Configure AWS-CLI for your Account. Make sure the default region matches the region in `serverless.yml`
- `aws configure`

##### Install dependencies
- `npm i`

##### Deploy Backend
- `sls deploy`

##### Build Client
- `npm run-script client:build`

##### Deploy Client
- `sls client deploy`

- - -
## Running locally

#### Run Client
- `npm run-script client:start`

**_Note_**: This will only work if you previously deployed the backend. If this fails, confirm you still have a `be-stack.json` file at the root of this project.

#### Run Backend
- `npm start`

If you want to point your local client to your local backend, edit your `be-stack.json` and set `ServiceEndpoint` to `http://localhost:3000`. Note that you will still be using the Cognito pools in AWS.

- - -
## Email subscription

DVSA sends receipts in the email (which will help you in hacking it). You can use the built-in **Inbox** page within the application to get the emails and obtain the receipts.

**_Note_**: each user will be assigned an email from `mailsac.com` which will be automatically verified. Real emails will be sent to their account and will appear in the application Inbox page. All this is **transparent** to the user and the deployer).

**_Note_**: to make the email verification script work your default AWS region has to be "US East (N. Virginia)", for example by setting `region = us-east-1` in your ~/.aws/config file

**Alternatively**, if you want users to receive emails to their registered email account (e.g. gmail), use one of the followings:

- Send an email verification link to email address, by running the following command (after clicking on the received link, emails will **also** be sent to their actual email address):

`aws ses verify-email-identity --email-address <your_email>`

- [Request a sending limit increase](https://console.aws.amazon.com/support/v1#/case/create?issueType=service-limit-increase&limitType=service-code-ses). This will allow your entire cloud account to send emails to any address.


- - -
## Presentation
[Download](OWASP_DC_SLS_Top10.pdf)



## Documentation

#### AWS ####

see [LESSONS](AWS/LESSONS/README.md) for information about hacking DVSA.

see [VIDEOS](AWS/VIDEOS) for how to deploy, use and hack DVSA.


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

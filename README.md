
# ![alt DVSA](https://i.imgur.com/25k8dtv.png) DVSA

## a Damn Vulnerable Serverless Application 

- - -
Damn Vulnerable Serverless Application (DVSA) is a deliberately vulnerable application aiming to be an aid for security professionals to test their skills and tools in a legal environment, help developers better understand the processes of securing serverless applications and to aid both students & teachers to learn about serverless application security in a controlled class room environment.

The aim of DVSA is to **practice some of the most common serverless vulnerabilities**, with a simple straightforward interface.

Please note, there are **both documented and undocumented vulnerabilities** with this software. This is intentional. You are encouraged to try and discover as many issues as possible.




- - - 
## Disclaimer

We do not take responsibility for the way in which any one uses this application (DVSA). We have made the purposes of the application clear and it should not be used maliciously. We have given warnings and taken measures to prevent users from installing DVSA on to production accounts.




- - -
## License
Damn Vulnerable Serverless Application (DVSA) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Damn Vulnerable Serverless Application (DVSA) is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Damn Vulnerable Serverless Application (DVSA).  If not, see http://www.gnu.org/licenses/.



- - -
## Deployment

- `clone`

- `npm install`

#### Deploy Backend
- `sls deploy` 

#### Build Client
- `npm run-script client:build` 

#### Deploy Client
- `sls client deploy` 


- - - 
## Documentation

**AWS**: see [LESSONS](AWS/LESSONS/README.md) for more information.


- - - 
## Links
[OWASP Top 10 - Serverless Interpretation](https://github.com/OWASP/Serverless-Top-10-Project/blob/master/README.md)

[Deep-Dive into Serverless Attacks - Series](https://www.protego.io/category/a-deep-dive-into-serverless-attacks/)

[OWASP Serverless Top 10 Project](https://www.owasp.org/index.php/OWASP_Serverless_Top_10_Project)

[Twitter account ](https://twitter.com/DVSAowasp) (hackable)

[Slack Channel #project-sls-top-10](https://owasp.slack.com/join/shared_invite/enQtNDI5MzgxMDQ2MTAwLTEyNzIzYWQ2NDZiMGIwNmJhYzYxZDJiNTM0ZmZiZmJlY2EwZmMwYjAyNmJjNzQxNzMyMWY4OTk3ZTQ0MzFhMDY)

- - -
## Acknowledgements
DVSA was created and contributed to OWASP by Tal Melamed, [Protego Labs](https://protego.io)

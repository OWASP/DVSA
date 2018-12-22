# LESSION 10: Unhandled Exceptions

The Lambda that handles the request is a "dumb" function when talking about response message. The function returns back any message that was received from the invoked function. In some cases, sending partial or incorrect data could reveal code or sensitive information if an error is sent back to to the function.

for example, using the partial payload:
```{"action": "get"}```

We will receive an error that reveils vode from the invoked function:
```
{"StatusCode":200,"FunctionError":"Unhandled","ExecutedVersion":"$LATEST","Payload":"{\"stackTrace\": [[\"/var/task/lambda_function.py\", 29, \"lambda_handler\", \"orderId = event[\\\"orderId\\\"]\"]], \"errorType\": \"KeyError\", \"errorMessage\": \"'orderId'\"}"}
```

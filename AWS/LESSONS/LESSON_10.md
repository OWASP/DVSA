# LESSON 10: Unhandled Exceptions

The Lambda that handles the request is a "dumb" function when talking about response message. The function returns back any message that was received from the invoked function. In some cases, sending partial or incorrect data could reveal code or sensitive information if an error is sent back to to the function.

For example, using the partial payload:
```{"action": "get"}```

We will receive an error that reveals code from the invoked function:
```
{
  "stackTrace": [
    [
      "/var/task/lambda_function.py",
      29,
      "lambda_handler",
      "orderId = event[\"orderId\"]"
    ]
  ],
  "errorType": "KeyError",
  "errorMessage": "'orderId'"
}
```

Another example (missing email):

```
{"action":"shipping","order-id":"61f6269a-aafd-406d-8dca-84873b6ccef5","data":{"name":"asdasda","address":"sdasdasd","email":"","phone":"123123123"}}
```

Will result in:
```
{
   "stackTrace":[
      [
         "/var/task/lambda_function.py",
         47,
         "lambda_handler",
         "':address': address"
      ],
      [
         "/var/runtime/boto3/resources/factory.py",
         520,
         "do_action",
         "response = action(self, *args, **kwargs)"
      ],
      [
         "/var/runtime/boto3/resources/action.py",
         83,
         "__call__",
         "response = getattr(parent.meta.client, operation_name)(**params)"
      ],
      [
         "/var/runtime/botocore/client.py",
         314,
         "_api_call",
         "return self._make_api_call(operation_name, kwargs)"
      ],
      [
         "/var/runtime/botocore/client.py",
         612,
         "_make_api_call",
         "raise error_class(parsed_response, operation_name)"
      ]
   ],
   "errorType":"ClientError",
   "errorMessage":"An error occurred (ValidationException) when calling the UpdateItem operation: ExpressionAttributeValues contains invalid value: One or more parameter values were invalid: An AttributeValue may not contain an empty string for key :address"
}
```



- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)

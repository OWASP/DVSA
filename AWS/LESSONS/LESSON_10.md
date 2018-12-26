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

- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)

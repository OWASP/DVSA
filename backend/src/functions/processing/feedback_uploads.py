import json
import time
import boto3
import os
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    try:
        response = s3.generate_presigned_url('get_object',
                                                Params={
                                                    'Bucket': os.environ["FEEDBACK_BUCKET"],
                                                    'Key': event["file"]},
                                                ExpiresIn=300)
    except ClientError as e:
        print str(e)
        return None

    return response
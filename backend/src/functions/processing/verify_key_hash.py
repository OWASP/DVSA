import json
import boto3
import botocore
import os


def lambda_handler(event, context):
    print(json.dumps(event))
    hash = {}
    if "Records" in event:
        records = event.get("Records")
        for record in records:
            if "s3" in record:
                try:
                    s3 = record.get("s3")
                    if "bucket" in s3 and "object" in s3:
                        bucket = s3.get("bucket")["name"]
                        key = s3.get("object")["key"]
                        if download_file(bucket, key):
                            md5 = get_file_hash(key)
                            hash[key] = md5.split(' ')[0]
                except:
                    pass
    return hash


def get_file_hash(k):
    if not os.path.isdir("/tmp/images"):
        os.mkdir("/tmp/images")
    os.system("md5sum /tmp/md5 >/tmp/" + k)
    #os.system("md5sum /tmp/md5 >/tmp/tmp")
    with open('/tmp/' + k) as f:
        r = f.read()
        

def download_file(b, k):
    try:
        s3 = boto3.client('s3')
        s3.download_file(b, k, '/tmp/md5')
    except:
        pass

    return True

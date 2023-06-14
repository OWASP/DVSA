import os
import json
import boto3
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", help="Deployment region")
    parser.add_argument("-p", "--profile", help="Deploymen profile")
    parser.add_argument("-s", "--stack", help="Serverless Stack Name")
    parser.add_argument("-b", "--bucket", help="DVSA website S3 bucket")
    parser.add_argument("-f", "--entire-folder", help="Upload the entire backend/deployment/dist_s3 folder (by default uploading only bundle.js)", action="store_true")
    return parser.parse_args()


def update_from_bucket_name(session, bucket, entire_folder):
    s3 = session.client('s3')
    dist_dir = "backend/deployment/dist_s3"
    try:
        get_bucket = s3.get_bucket_website(Bucket=bucket)
        if "IndexDocument" in get_bucket:
            for subdir, dirs, files in os.walk(dist_dir):
              for file in files:
                  key = os.path.join(subdir, file).replace(f"{dist_dir}/", "")
                  if not entire_folder and os.path.join(subdir, file) != f"{dist_dir}/bundle.js":
                      pass
                  else:
                      print(f"\t. Uploading {dist_dir}/{key} to s3://{bucket}/{key}...", end="")
                      try:
                          res = s3.upload_file(f"{dist_dir}/{key}", bucket, key)
                          print("OK")
                      except Exception as e:
                          print(f"FAILED")
                          print(e)
                          return
    except:
        print(f"Failed to identify DVSA-website bucket: {bucket}. Wrong bucket?")
        return
    print("client-update completed successfully!")


def update_from_stack_name(session, stack_name, entire_folder):
    cf = session.client('cloudformation')
    try:
        stack_sum = cf.list_stacks().get("StackSummaries", [])
    except Exception as e:
        print(e)

    if len(stack_sum) == 0:
        print(f"[X] Could not find ANY stack under the account/region provided.")
        return
    
    else:
        identified_stack = None
        for stack in stack_sum:
            if stack["StackName"] == stack_name:
                identified_stack = stack["StackName"]
                break
            
        if identified_stack is None:
            print(f"[X] Could not find stack: {stack_name} in the account/region provided.")
            return
        
        else:
            print("[-] Stack found. Trying to location website-bucket... ", end="")
            try:
                resources = cf.list_stack_resources(StackName=identified_stack).get("StackResourceSummaries", [])
            except Exception as e:
                print(e)

            stack_buckets = []
            for rsc in resources:
                if rsc["ResourceType"] == "AWS::S3::Bucket":
                    if rsc["LogicalResourceId"] == "S3WebsiteBucket":
                        print("OK")
                        return update_from_bucket_name(session, rsc["PhysicalResourceId"], entire_folder)
                    else:
                        stack_buckets.append(f"\t. {rsc['PhysicalResourceId']}")

            print("FAILED")
            print(f"Could not identify the website bucket. Did you change the default template name?")
            if len(stack_buckets)>0:
                print("The following buckets were found. Run again with --bucket and specify the website-bucket.")
                print(''.join(stack_buckets))



def main():
    args = get_args()
    session = boto3.session.Session(profile_name=args.profile, region_name=args.region)
    aws_region = session.region_name
    sts = session.client('sts')
    account_id = sts.get_caller_identity().get("Account")

    if args.stack is not None:
        stack = args.stack
        print(f"[-] Looking for CloudFormation Stack: {stack} in: {account_id}/{aws_region}")
        return update_from_stack_name(session, stack, args.entire_folder)

    elif args.bucket is not None:
        bucket = args.bucket
        print(f"[-] Looking for S3 Bucket: {bucket} in: {account_id}/{aws_region}")
        return update_from_bucket_name(session, bucket, args.entire_folder)

    else:
        print("[!] You must specify either the DVSA-Website S3 bucket name or the DVSA Stack-name.")
        return

if __name__ == "__main__":
    main()

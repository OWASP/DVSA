import os
import boto3
from hashlib import md5
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", help="Deployment region")
    parser.add_argument("-p", "--profile", help="Deploymen profile")
    parser.add_argument("-t", "--template", help="The template file (default: template.yml)", default="template.yml")
    parser.add_argument("-s3", "--s3-repo", help="The S3 bucket to store the repo files")
    parser.add_argument("-o", "--output-file", help="the packaged yaml file", default="packaged-template.yml")
    parser.add_argument("-v", "--verbose", help="Debug mode", action="store_true")
    parser.add_argument("-f", "--force-upload", help="Force uploading files", action="store_true")
    return parser.parse_args()


def main():
  args = get_args()
  session = boto3.session.Session(profile_name=args.profile, region_name=args.region)
  
  print("[-] Validating template... ")
  cmd = f"sam validate --template {args.template} --lint"
  print(f"Running command:\n\t. {cmd}")
  os.system(cmd)

  print("[-] Building backend... ")
  cmd = f"sam build --template {args.template} --parallel"
  cmd = cmd + " --debug" if args.verbose else cmd
  print(f"Running command:\n\t. {cmd}")
  os.system(cmd)

  # package template into sam yaml file
  print("[-] Creating a new template with the new code... ")
  cmd = f"sam package --output-template-file {args.output_file}"
  cmd = cmd + " --resolve-s3" if args.s3_repo is None else cmd + f" --s3-repo {args.s3_repo}"
  cmd = cmd + f" --profile {session.profile_name} --region {session.region_name}"
  cmd = cmd + " --debug" if args.verbose else cmd
  cmd = cmd + " --force-upload" if args.force_upload else cmd
  print(f"Running command:\n\t. {cmd}")
  os.system(cmd)

  print("\t\t\t\t******************************\n")
  print("Your packaged template was created successfully!!")
  print(f"You can now use $ sam deploy or create/update a stack by uploading {args.output_file} through the CloudFormation console/cli")
  return

if __name__ == "__main__":
  main()

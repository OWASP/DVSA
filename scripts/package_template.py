import json
import os
import boto3
from hashlib import md5
import re
import argparse
import shutil




sam_file = "sam_packaged.yml"
tmp_s3 = "dvsa.serverless.repo"
sam_final = "sam.yaml"
cwd = os.getcwd()

aws_regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ap-northeast-1", "eu-central-1", "eu-west-1", "eu-south-1", "eu-north-1"]



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", help="Deployment region (default: us-east-1)", default="us-east-1")
    parser.add_argument("-p", "--profile", help="Deploymen profile (default: default)", default="default")
    parser.add_argument("-d", "--delete", help="Delete App from Repository", action="store_true")
    parser.add_argument("-f", "--force", help="Force delete/deployment", action="store_true")
    parser.add_argument("-v", "--version", help="Update to sepecific version", default="auto")
    parser.add_argument("-t", "--template", help="The template file (default: template.yml)", default="template.yml")
    parser.add_argument("-s3", "--s3-repo", help="The S3 bucket to store the repo files (default: dvsa.serverless.repo)", default="dvsa.serverless.repo")
    parser.add_argument("-c", "--build-client", help="Rebuild client", action="store_true")
    parser.add_argument("-i", "--debug", help="Debug mode", action="store_true")
    return parser.parse_args()


def pack_dist():
  # replace parameters with placeholders
  client_dist = "client/dist"
  deployment_dist = "backend/deployment/dist_s3"
  be_stack_file = "client/src/be-stack.json"

  print("[-] replacing placeholders with deployment parameters")
  with open(be_stack_file) as f:
    stack = json.loads(f.read())

  with open(f"{client_dist}/bundle.js", "r") as fr:
    bundle = fr.read()

  for item in stack:
    k,v = item,stack[item]
    placeholder = "<{}>".format(k)
    print(f"replacing: {placeholder} with: {v}... ", end="")
    bundle = bundle.replace(placeholder, v)
    if bundle.find(v) > -1 and bundle.find(placeholder) == -1:  
      print("OK")
    else:
      print("FAILED")

  print("[-] copying dist folder to s3_dist")
  if os.path.exists(deployment_dist):
    shutil.rmtree(deployment_dist)
  shutil.copytree(client_dist, deployment_dist)
  with open(f"{deployment_dist}/bundle.js", "w") as f:
    f.write(bundle)
    f.close()
  return 


def update_template_version(infile, v):
  os.chdir(cwd)
  with open(infile) as f:
    template = f.read()
  old_version = re.search(r"[0-9][.][0-9][.][0-9]{1,3}", template).group()
  if v == "auto":
    version = old_version.split(".")
    sub_inc =  int(version[2]) + 1
    new_version = f"{version[0]}.{version[1]}.{sub_inc}"
    print("[-] incrementing {} from: {} to: {}".format(infile, old_version, new_version))
  else:
    print("[-] manually setting version to: {}".format(v))
    new_version = v

  new_template = template.replace(old_version, new_version)
  with open(infile, "w") as f:
    f.write(new_template)
  return new_version



def main():
  args = get_args()
  profile = args.profile
  xregion = args.region

  s3_repo = args.s3_repo
  build_client = args.build_client
  template_file = args.template

  if xregion == "all":
    regions = aws_regions
  elif ',' in xregion:
    regions = xregion.split(',')
  else:
    regions = [xregion]

  
  session = boto3.session.Session(profile_name=profile)

  # --delete
  if args.delete:
    print("[-] Deleting app from repo")
    if not args.force:
      concent = input("[!] About to empty S3 [{}], would you like to continue [y/N]? > ".format(s3_repo))
      if concent.lower() != "y":
        print("cancelling...")
        return

    s3 = session.resource('s3')
    bucket = s3.Bucket(s3_repo)
    bucket.objects.all().delete()
    return

  
  # client-side website
  if not build_client:
    print("[!] Did not use (-c/--client) to rebuild client-side, skipping.")
  else:
    print("[!] Rebuilding client-side!")
    os.system("npm i")
    os.system("npm run-script client:build")

  # getting client/dist folder and adding placeholsers
  pack_dist()

  # build function (SAM)
  cmd = f"sam build --template {template_file} --parallel"
  print(f"Running command: {cmd}")
  os.system(cmd)


  # package template into sam yaml file
  print("[-] packaging template into sam yaml file")
  template_hash = -1
  try:
    if os.path.exists(sam_file) and not args.force:
      with open(sam_file, 'rb') as f:
        template_hash = md5(f.read()).hexdigest()
    os.remove(sam_file)
  except OSError:
      pass
      
  template_file = args.template

  cmd = f"sam package --output-template-file {sam_file} --s3-bucket {s3_repo} --profile {profile}"
  cmd = cmd + " --debug" if args.debug else cmd
  print(f"Running command: {cmd}")
  os.system(cmd)
  new_hash = 0
  if not args.force and template_hash != -1:
    with open(sam_file, 'rb') as f:
      new_hash = md5(f.read()).hexdigest()


  if template_hash != new_hash:
    new_version = update_template_version(template_file, args.version)
    update_template_version(sam_file, new_version)

    for region in regions:
      print(f"[-] attempting to publish sam template on region: {region}")
      if os.path.isfile(sam_file):
        cmd = "sam publish --template {} --profile {} --region {}".format(sam_file, profile, region)
        cmd = cmd + " --debug" if args.debug else cmd
        print(f"Running command: {cmd}")
        os.system(cmd)
      
      else:
        print("[!] sam package wasn't found.")

  else:
    print("Nothing was changed...")


if __name__ == "__main__":
  main()

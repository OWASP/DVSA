import json
import boto3
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", help="Deployment region")
    parser.add_argument("-p", "--profile", help="Deploymen profile")
    parser.add_argument("-s", "--stack", help="Serverless Stack Name", required=True)
    return parser.parse_args()


def build_be_stack(resources):
    be_stack_file = "be-stack.json"
    new_stack = {
        "ServiceEndpoint": "https://<GATEWAY_API>.execute-api.eu-central-1.amazonaws.com/<GATEWAY_STAGE>"
    }

    for r in resources:
        if r["ResourceType"] == "AWS::Cognito::IdentityPool":
            new_stack["IdentityPoolId"] = r["PhysicalResourceId"]

        elif r["ResourceType"] == "AWS::Cognito::UserPool":
            new_stack["UserPoolId"] = r["PhysicalResourceId"]

        elif r["ResourceType"] == "AWS::Cognito::UserPoolClient":
            new_stack["UserPoolClientId"] = r["PhysicalResourceId"]

        elif r["ResourceType"] == "AWS::ApiGateway::RestApi":
            new_stack["ServiceEndpoint"] = new_stack["ServiceEndpoint"].replace("<GATEWAY_API>", r["PhysicalResourceId"])

        elif r["ResourceType"] == "AWS::ApiGateway::Stage":
            new_stack["ServiceEndpoint"] = new_stack["ServiceEndpoint"].replace("<GATEWAY_STAGE>", r["PhysicalResourceId"])
            
        else:
            pass  
        
    if new_stack["ServiceEndpoint"].find("<GATEWAY_API>") > -1 or new_stack["ServiceEndpoint"].find("<GATEWAY_STAGE>") > -1:
        print("[X] Something went wrong. Could not identify all relevant resource in stack.")
        print(f"Found the following data...\n {json.dumps(new_stack)}")
        return False

    for k in new_stack:
        print(f"\t. Updating {k} placeholder with: {new_stack[k]}... ", end="")
        print("OK")

    with open(f"client/src/{be_stack_file}", "w") as f:
        f.write(json.dumps(new_stack))
        f.close()

    return True


def main():
    args = get_args()
    session = boto3.session.Session(profile_name=args.profile, region_name=args.region)
    aws_region = session.region_name
    sts = session.client('sts')
    account_id = sts.get_caller_identity().get("Account")
    stack_name = args.stack
    print(f"[-] Looking for Stack: {stack_name} in: {account_id}/{aws_region}")
    cf = session.client('cloudformation')

    try:
        stack_sum = cf.list_stacks().get("StackSummaries", [])
    except Exception as e:
        print(e)

    if len(stack_sum) == 0:
        print(f"[X] Could not find ANY stack in: {account_id}/{aws_region}. Maybe a different region?")
        return
    
    else:
        identified_stack = None
        available_stacks = []
        for stack in stack_sum:
            if stack["StackName"] == stack_name:
                identified_stack = stack["StackName"]
                break
            elif stack["StackStatus"] != "DELETE_COMPLETE":
                available_stacks.append(f"\t. {stack['StackName']}\n")
            else:
                pass
            
        if identified_stack is None:
            print(f"[X] Could not identify stack: {stack_name} in: {account_id}/{aws_region}")
            print(f"[?] Could be any of those:\n {''.join(available_stacks)}")
            return
        
        else:
              print(f"[-] Collecting stack info... ")
              try:
                  resources = cf.list_stack_resources(StackName=identified_stack).get("StackResourceSummaries", [])
              except Exception as e:
                  print(e)

              if not build_be_stack(resources):
                  return
              
              else:
                  print("client-connect completed successfully!")
    return


if __name__ == "__main__":
    main()

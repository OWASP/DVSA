import json
import datetime
import time
import random
import string
import boto3



def get_sum(ccn):
    sum = 0
    num_digits = len(str(ccn))
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(ccn[count])
        if not count & 1 ^ oddeven:
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit

    return sum


def lambda_handler(event, context):
    n = random.randint(2, 4)  # this is to play the role of an external service.
    time.sleep(n)
    data = json.loads(event["body"])
    ccn = data['ccn']
    exp_m = int(data['exp'].split("/")[0])
    exp_y = int(data['exp'].split("/")[1]) + 2000
    d = datetime.datetime.today()

    ccn_sum = get_sum(ccn)

    if (ccn_sum % 10) == 0:
        if len(str(data['cvv'])) != 3:
            res = {"status": 110, "msg": "invalid cvv"}

        elif (exp_y < d.year) or (exp_y == d.year and exp_m <= d.month) or (exp_m < 1) or (exp_m > 12) or (
                exp_y > 2099):

            res = {"status": 110, "msg": "invalid expiration date"}

        else:
            token = ''.join(
                random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(12))
            res = {"status": 120, "confirmation_token": token}
    else:
        res = {"status": 110, "msg": "invalid payment data"}

    return {
        'statusCode': 200,
        'body': json.dumps(res)
    }

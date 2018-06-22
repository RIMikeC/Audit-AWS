# audit_aws.py
#
# By Mike C
#
# 15th June 2018
#
# Collect AWS resources for Ireland

# Get SDK and other useful bits

import boto3
import sys
import json
import datetime

bucket_name='ri-aws-audit'
todays_date=str(datetime.date.today())

try:
    ec2=boto3.client('ec2',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to EC2 client")
    sys.exit(1)

try:
    asg=boto3.client('autoscaling',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to ASG client")
    sys.exit(1)

try:
    ecs=boto3.client('ecs',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to ECS client")
    sys.exit(1)

try:
    s3=boto3.client('s3',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to s3 client")
    sys.exit(1)

try:
    sts=boto3.client('sts',region_name = 'eu-west-1')
    account_id=sts.get_caller_identity()['Account']
except Exception as e:
    print(e,": failed to connect to STS client")
    sys.exit(1)

try:
    lambs=boto3.client('lambda')
except Exception as e:
    print(e,": failed to connect to lambda client")
    sys.exit(1)

def lambda_handler(event, context):  

    ec2_count=0
    response=ec2.describe_instances()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_ec2.json'.format(account_id, todays_date), Body=json.dumps(response['Reservations'], indent=4, sort_keys=True, default=str))
    for i in response['Reservations']:
        ec2_count=ec2_count+len(i['Instances'])

    response=asg.describe_auto_scaling_groups()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_asg.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str))

    response=lambs.list_functions()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_lambdas.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str))
    lambda_count=len(response['Functions'])

    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/stats.json'.format(account_id, todays_date), Body=json.dumps({'Date':'121212','User':'1234456773','Stats':[{'EC2':'1','ASG':'2','lambda':'3'}]}, indent=4))

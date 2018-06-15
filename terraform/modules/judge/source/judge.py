# judge.py
#
# By Mike C
#
# 25th June 2018
#
# Collect AWS resources for Ireland

# Get SDK and other useful bits

import boto3
import sys
import json
import urllib.parse
import datetime

bucket_name='ri-aws-audit'

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
except Exception as e:
    print(e,": failed to connect to sts client")
    sys.exit(1)


account_id=sts.get_caller_identity()['Account']

def lambda_handler(event, context):  
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("bucket is: ",bucket)
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("key is: ",key)
    print()
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        json_data = response['Body'].read()
        print(json_data)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


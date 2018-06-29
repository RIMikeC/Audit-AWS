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
import time

bucket_name='ri-aws-audit'

try: ec2=boto3.client('ec2',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to EC2 client")
    sys.exit(1)

try: asg=boto3.client('autoscaling',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to ASG client")
    sys.exit(1)

try: ecs=boto3.client('ecs',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to ECS client")
    sys.exit(1)

try: s3=boto3.client('s3',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to s3 client")
    sys.exit(1)

try:
    sts=boto3.client('sts',region_name = 'eu-west-1')
    account_id=sts.get_caller_identity()['Account']
except Exception as e:
    print(e,": failed to connect to sts client")
    sys.exit(1)

try: cw=boto3.client('cloudwatch',region_name = 'eu-west-1')
except Exception as e:
    print("ERROR: failed to connect to CloudWatch")
    sys.exit(1)

def mark_ec2(data):
    print("fake marking ec2")
    return(2)

def mark_asg(data):
    not_scaling=0
    for asg_map in data['AutoScalingGroups']:
        if asg_map['DesiredCapacity']==asg_map['MinSize']==asg_map['MaxSize']: not_scaling=not_scaling+1
    print(int(100*not_scaling/len(data['AutoScalingGroups'])))
    put_cw_metric('Scalability',int(100*not_scaling/len(data['AutoScalingGroups'])),'Percent')
    return

def mark_lambdas(data):
    lamba_count=len(data['Functions'])


def mark_serverlessness(ins,lams):
    time.sleep(1)
    print("serverlessness ",ins,lams)
    return()

def put_cw_metric(metric_name,metric_value,metric_units):
    try:
        cw.put_metric_data(
            Namespace='Audit',
            MetricData=[{
                'MetricName': metric_name,
                'Dimensions': [{'Name': 'USER', 'Value': account_id}],
                'Value': metric_value
                'Unit': metric_units
            }]
        )
    except ClientError as e: print(e.response['Error']['Message'])
    return

def lambda_handler(event, context):  
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("bucket is: ",bucket,"   key is: ",key)
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    json_data = response['Body'].read()
    data = json.loads(json_data)

    lambda_count=0
    
    if   'all_ec2.json'     in key: mark_ec2(data)
    elif 'all_asg.json'     in key: mark_asg(data)
    elif 'all_lambdas.json' in key: mark_lambdas(data)



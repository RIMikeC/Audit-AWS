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
object_name='test.txt'

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

#response=ec2.describe_instances()
#
#s3.put_object(Bucket=bucket_name, Key='audit/{}/ec1.json'.format(account_id), Body=json.dumps(response['Reservations'], indent=4))
#
#for reservation in response['Reservations']:
#    for instance in reservation['Instances']:
#        print("Adding EC2")
#
#        s3.put_object(Bucket=bucket_name, Key='audit/{}/ec2.json'.format(account_id), Body=json.dumps({instance['InstanceId']:[{'AMI':instance['ImageId'],'Size':instance['InstanceType'],'Tags':[{'Key':'k','Value':'v'}]}]}, indent=4))

    response=asg.describe_auto_scaling_groups()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/all_asg.json'.format(account_id), Body=json.dumps(response, indent=4, sort_keys=True, default=str))
    for group in response['AutoScalingGroups']:
        s3.put_object(Bucket=bucket_name, Key='audit/{}/asg.{}json'.format(account_id,group['AutoScalingGroupName']), Body=json.dumps({group['AutoScalingGroupName']:[{'Min':group['MinSize'],'Max':group['MaxSize'],'Desired':group['DesiredCapacity'],'Current':len(group['Instances'])}]}, indent=4))
    


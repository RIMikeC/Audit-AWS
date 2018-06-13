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

bucket_name='ri-aws-audit'
object_prefix='testdev'
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

#def lambda_handler(event, context):  

response=ec2.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        s3.put_object(Bucket=bucket_name, Key='{}/containers.json'.format(object_prefix), Body=json.dumps({instance['InstanceId']:[{'AMI':instance['ImageId'],'Size':instance['InstanceType']}]}, indent=4))
        print("hi")

response=asg.describe_auto_scaling_groups()
for group in response['AutoScalingGroups']:
    s3.put_object(Bucket=bucket_name, Key='{}/containers.json'.format(object_prefix), Body=json.dumps({group['AutoScalingGroupName']:[{'Min':group['MinSize'],'Max':group['MaxSize'],'Desired':group['DesiredCapacity'],'Current':len(group['Instances'])}]}, indent=4))
    print("hi")

response=ecs.list_clusters()
for cluster_arn in response['clusterArns']:
    container_instances=ecs.list_container_instances(cluster=cluster_arn)
    s3.put_object(Bucket=bucket_name, Key='{}/containers.json'.format(object_prefix), Body=json.dumps({cluster_arn:{'Instance':[container_instances]}}, indent=4))
    print("hi")


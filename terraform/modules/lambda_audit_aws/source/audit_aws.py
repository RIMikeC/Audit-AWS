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
import datetime
import json

try:
    ec2=boto3.client('ec2',region_name = 'eu-west-1')
except Exception as e:
    print("ERROR: failed to connect to EC2 client")
    sys.exit(1)

try:
    asg=boto3.client('autoscaling',region_name = 'eu-west-1')
except Exception as e:
    print("ERROR: failed to connect to ASG client")
    sys.exit(1)

try:
    ecs=boto3.client('ecs',region_name = 'eu-west-1')
except Exception as e:
    print("ERROR: failed to connect to ECS client")
    sys.exit(1)

#def lambda_handler(event, context):  
#todays_date=datetime.date.today()

response=ec2.describe_instances()
print("ID,AMI,Size")
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(instance['InstanceId'],instance['ImageId'],instance['InstanceType'],sep=',')

print()

response=ec2.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(json.dumps({instance['InstanceId']:[{'AMI':instance['ImageId'],'Size':instance['InstanceType']}]}, indent=4))

print()

response=asg.describe_auto_scaling_groups()
print("ASG,Min,Max,Desired,Current")
for group in response['AutoScalingGroups']:
    print(group['AutoScalingGroupName'],group['MinSize'],group['MaxSize'],group['DesiredCapacity'],len(group['Instances']),sep=',')

print()

response=asg.describe_auto_scaling_groups()
for group in response['AutoScalingGroups']:
    print(json.dumps({group['AutoScalingGroupName']:[{'Min':group['MinSize'],'Max':group['MaxSize'],'Desired':group['DesiredCapacity'],'Current':len(group['Instances'])}]}, indent=4))

print()

response=ecs.list_clusters()
print("Cluster,Registered Container Instance")
for cluster_arn in response['clusterArns']:
    container_instances=ecs.list_container_instances(cluster=cluster_arn)
    for container_instance in container_instances['containerInstanceArns']:
        print(cluster_arn,container_instance,sep=',')

print()

response=ecs.list_clusters()
for cluster_arn in response['clusterArns']:
    container_instances=ecs.list_container_instances(cluster=cluster_arn)
    print(json.dumps({cluster_arn:{'Instance':[container_instances]}}, indent=4))


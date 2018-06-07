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

try:
    ec2=boto3.client('ec2',region_name = 'eu-west-1')
except Exception as e:
    print("ERROR: failed to connect to EC2 client")
    sys.exit(1)

#def lambda_handler(event, context):  
todays_date=datetime.date.today()
response=ec2.describe_instances()
print("ID,AMI,Size,Public IP,Private IP")
for instance in response['Reservations'][0]['Instances']:
    print(instance['InstanceId'],instance['ImageId'],instance['InstanceType'],instance['PublicIpAddress'],instance['PrivateIpAddress'],sep=',')


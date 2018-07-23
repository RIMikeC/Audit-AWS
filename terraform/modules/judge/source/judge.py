# judge.py
#
# By Mike C
#
# 5th July 2018
#
# Collect AWS resources for Ireland

# Get SDK and other useful bits

import boto3
import sys
import json
import urllib

# Open the SDK clients

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

# Award marks to the EC2 instances

def mark_ec2s(data):
    print("fake marking ec2")
    return(2)

# Award marks for scalability ie use of ASGs

def mark_scalability(data):
    not_scaling=0
    for asg_map in data['AutoScalingGroups']:
        if asg_map['DesiredCapacity']==asg_map['MinSize']==asg_map['MaxSize']: not_scaling=not_scaling+1
    put_cw_metric('Scalability',int(100*not_scaling/len(data['AutoScalingGroups'])),'Percent')
    return

# Award marks for the percentage of workloads that are serverless

def mark_serverlessness(data):
    put_cw_metric('Severlessness',int((data['Statistics'][0]['ResourceCounts'][0]['lambda']*100)/(data['Statistics'][0]['ResourceCounts'][0]['EC2']+data['Statistics'][0]['ResourceCounts'][0]['lambda'])),'Percent')
    return

# Find the percentage of tags that should be used that actually have been used

def mark_tags(data):
    counts=data['Statistics'][0]['ResourceCounts'][0]
    print("taggable itema ",counts['Subnets']+counts['NATGateways']+['VPC']+['Volumes']+['SecurityGroups']+['RouteTables']+['EC2']+['InternetGW'])
    print("Tags used ",counts['Tag'],counts['NATGateways'],counts['VPC'],counts['Volumes'],counts['SecurityGroups'])
    print("more ",counts['RouteTables'],counts['EC2'],counts['InternetGW'])
    print("total correct tags used ",counts['Tag'])
    


# The following stanza sends the value passed as a parameter to CW as a custom metric in the 'Audit' namespace

def put_cw_metric(metric_name,metric_value,metric_units):
    try:
        cw.put_metric_data(
            Namespace='Audit',
            MetricData=[{
                'MetricName': metric_name,
                'Dimensions': [{'Name': 'USER', 'Value': account_id}],
                'Value': metric_value,
                'Unit': metric_units
            }]
        )
    except ClientError as e: print(e.response['Error']['Message'])
    return

# lambda_handler is the default name of the entry point for lambda

def lambda_handler(event, context):  
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    json_data = response['Body'].read()
    data = json.loads(json_data)

    lambda_count=0
    
    if   'all_ec2s.json' in key: mark_ec2s(data)
    elif 'all_asgs.json' in key: mark_scalability(data)
    elif 'stats.json'    in key: 
        mark_serverlessness(data)
        mark_tags(data)

# subnets
#for i in data['Subnets']:
#     if '10.20' in i['CidrBlock']:
#         i['AvailabilityZone'],i['AvailableIpAddressCount'],i['CidrBlock'],i['SubnetId']



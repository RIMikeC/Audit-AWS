
import boto3
import json
s3=boto3.client('s3',region_name = 'eu-west-1')
bucket='ri-aws-audit'
key='audit/460402331925/2018-06-21/all_asg.json'
response = s3.get_object(Bucket=bucket, Key=key)
json_data = response['Body'].read()
data = json.loads(json_data)

not_scaling=0
for asg_map in data['AutoScalingGroups']:
    if asg_map['DesiredCapacity']==asg_map['MinSize']==asg_map['MaxSize']:
        not_scaling=not_scaling+1
print(int(100*not_scaling/len(data['AutoScalingGroups'])))



# Get SDK and other useful bits

import boto3
import sys
import json
import datetime

bucket_name='ri-aws-audit'
todays_date=str(datetime.date.today())
audit_tags='&project=audit&programme=audit&product=audit&environment=production&cost_centre=81150&security_class=public&repo=RIMikeC/Audit-AWS&terraform=true'

try:
    ec2=boto3.client('ec2',region_name = 'eu-west-1')
except Exception as e:
    print(e,": failed to connect to EC2 client")
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

# Get the EC2 instances

ec2_count=0
response=ec2.describe_instances()
s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_ec2s.json'.format(account_id, todays_date), Body=json.dumps(response['Reservations'], indent=4, sort_keys=True, default=str), Tagging='Name=all_ec2s'+audit_tags)
for i in response['Reservations']:
    ec2_count=ec2_count+len(i['Instances'])


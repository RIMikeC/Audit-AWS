# audit_aws.py
#
# By Mike C
#
# 30th June 2018
#
# Collect AWS resources for Ireland

# Get SDK and other useful bits

import boto3
import sys
import json
import datetime

bucket_name='ri-aws-audit'
todays_date=str(datetime.date.today())
audit_tags='&project=audit&programme=audit&product=audit&environment=production&cost_centre=81150&security_class=public&repo=RIMikeC/Audit-AWS&terraform=true'

# Get the low-level clients

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
    print(e,": failed to connect to STS client")
    sys.exit(1)

try: lambs=boto3.client('lambda')
except Exception as e:
    print(e,": failed to connect to lambda client")
    sys.exit(1)

try: kinesis=boto3.client('kinesis')
except Exception as e:
    print(e,": failed to connect to kinesis client")
    sys.exit(1)

try: rds=boto3.client('rds')
except Exception as e:
    print(e,": failed to connect to rds client")
    sys.exit(1)

def lambda_handler(event, context):  

    # Each of the following sections uses an SDK low-level client to describe an AWS resource, then writes that output as a new S3 object.
    # The format of the object is JSON and mirrors the reposne to an API call such as https://ec2.amazonaws.com/?Action=DescribeInstances

    # Get the EC2 instances

    ec2_count=0
    response=ec2.describe_instances()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_ec2s.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_ec2s'+audit_tags)
    for i in response['Reservations']:
        ec2_count=ec2_count+len(i['Instances'])

    # Get the auto-scaling groups

    response=asg.describe_auto_scaling_groups()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_asgs.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_asgs'+audit_tags)
    asg_count=len(response['AutoScalingGroups'])

    # Get the lambda functions

    response=lambs.list_functions()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_lambdas.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_lambdas'+audit_tags)
    lambda_count=len(response['Functions'])

    # Get the virtual private clouds

    response=ec2.describe_vpcs()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_vpcs.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_vpcs'+audit_tags)
    vpc_count=len(response['Vpcs'])

    # Get the subnets

    response=ec2.describe_subnets()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_subnets.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_subnets'+audit_tags)
    subnet_count=len(response['Subnets'])

    # Get the internet gateways
    
    response=ec2.describe_internet_gateways()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_igws.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_igws'+audit_tags)
    subnet_count=len(response['InternetGateways'])

    # Get the route tables

    response=ec2.describe_route_tables()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_routetables.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_routetables'+audit_tags)
    subnet_count=len(response['RouteTables'])

    # Get the buckets

    response=s3.list_buckets()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_buckets.json'.format(account_id, todays_date), Body=json.dumps(response,indent=4, sort_keys=True, default=str), Tagging='Name=all_buckets'+audit_tags)
    bucket_count=len(response['Buckets'])

    # Get the peering connections

    response=ec2.describe_vpc_peering_connections()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_peering.json'.format(account_id, todays_date), Body=json.dumps(response,indent=4, sort_keys=True, default=str), Tagging='Name=all_peering'+audit_tags)
    peer_count=len(response['VpcPeeringConnections'])

    # Get the EC2 container clusters

    response=ecs.list_clusters()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_ecs.json'.format(account_id, todays_date), Body=json.dumps(response,indent=4, sort_keys=True, default=str), Tagging='Name=all_ecs'+audit_tags)
    ec2containercluster_count=len(response['clusterArns'])

    # Get the Kinesis streams

    response=kinesis.list_streams()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_streams.json'.format(account_id, todays_date), Body=json.dumps(response,indent=4, sort_keys=True, default=str), Tagging='Name=all_streams'+audit_tags)
    stream_count=len(response['StreamNames'])

    # Get the RDS clusters

    response=rds.describe_db_clusters()
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_rds.json'.format(account_id, todays_date), Body=json.dumps(response,indent=4, sort_keys=True, default=str), Tagging='Name=all_rds_clusters'+audit_tags)
    rds_cluster_count=len(response['DBClusters'])

    # Get the tags

    response=ec2.describe_tags(Filters=[{'Name':'key','Values':['Name','programme','cost_centre','environment','security_class','repo','terraform','project','product']}])
    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/all_tags.json'.format(account_id, todays_date), Body=json.dumps(response, indent=4, sort_keys=True, default=str), Tagging='Name=all_tags'+audit_tags)
    tag_count=len(response['Tags'])

    # Create a new object, which contains statistics collected by the lines above

    s3.put_object(Bucket=bucket_name, Key='audit/{}/{}/stats.json'.format(account_id, todays_date), Body=json.dumps({"Statistics":[{'Date':todays_date,'User':account_id,'ResourceCounts':[{'EC2':ec2_count,'lambda':lambda_count,'ASG':asg_count,'VPC':vpc_count,'Subnet':subnet_count,'Bucket':bucket_count,'Peer':peer_count,'Tag':tag_count,'ECSclusters':ec2containercluster_count,'Streams':stream_count,'RDSClusters':rds_cluster_count}]}]}, indent=4), Tagging='Name=stats'+audit_tags)


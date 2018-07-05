[![forthebadge](https://forthebadge.com/images/badges/made-with-crayons.svg)](https://forthebadge.com)

# Audit-AWS

This is the repo for our AWS Audit

# Description

Our AWS infrastructure is audited daily between midnight and 9:30 am.
This repo contains the audit code, which is in Python 3.6. It is delivered using Terraform.

## FAQ

- Why do we need auditing?
With product teams able and willing to create/destroy their own infrastructure, then a good AWS-wide audit tool is vital for central governance and oversight.
- Where is the output stored?
In an appropriately secured bucket only
- Is there any sensitive data in the audit?
No, it is classified as public for security purposes, even though there is no public access
- How much does it cost to run an audit?
About $1 per month
- How do I run it?
It should be triggered as a CloudWatch event, to be run once a day at a time convenient to yourself between midnight and 9:30 am
- What permissions does the audit have?
It has read-only permissions for across almost all AWS resources. The exception is that it has write access to s3 in order to record the results


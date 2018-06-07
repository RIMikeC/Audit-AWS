# This module creates a role used by lambda functions
# and attaches a policy to it that gives it minimal access

## Inputs

| Name | Description | Default | Required |
|------|-------------|:-----:|:-----:|
| region | AWS region in which to execute | - | yes |
| account_id | account that the role runs under | - | yes |

## Outputs

| Name | Description |
|------|-------------|
| aws_audit_lambda_common_role_arn | ARN of the role created |


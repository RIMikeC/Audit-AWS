# lambda_audit_aws

This module collects stuff from AWS
and sticks it into a bucket


## Inputs

| Name | Description | Default | Required |
|------|-------------|:-----:|:-----:|
| lambda_role | Name of the IAM role to use | - | yes |
| audit_schedule | Cron expression which shows when to invoke the audit lambda | cron(0,20,40 * * * ? *) | no |

## Outputs

| Name | Description |
|------|-------------|
| None | n/a |

## Example Usage

```hcl
module jump {
  source         = "../../modules/lambda_audit_aws"
  lambda_role = "lambda_common"
}
```


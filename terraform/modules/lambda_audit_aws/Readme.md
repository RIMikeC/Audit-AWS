# lambda_audit_aws

This module collects stuff from AWS
and sticks it into a bucket

The name of the bucket is hard-coded, so that everyone uses the same one


## Inputs

| Name | Description | Default | Required |
|------|-------------|:-----:|:-----:|
| audit_schedule | Cron expression which shows when to invoke the audit lambda | cron(0,20,40 * * * ? *) | no |

## Outputs

| Name | Description |
|------|-------------|
| None | n/a |

## Example Usage

```hcl
module jump {
  source         = "../../modules/lambda_audit_aws"
}
```


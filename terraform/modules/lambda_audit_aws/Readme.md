# lambda_audit_aws

This module collects stuff from AWS
and sticks it into a bucket


## Inputs

| Name | Description | Default | Required |
|------|-------------|:-----:|:-----:|
| lambda_role | Name of the IAM role to use | - | yes |

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


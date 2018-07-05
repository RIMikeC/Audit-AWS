
data "aws_caller_identity" "current" {}

output "account_id" {
  value = "${data.aws_caller_identity.current.account_id}"
}

output "caller_arn" {
  value = "${data.aws_caller_identity.current.arn}"
}

output "caller_user" {
  value = "${data.aws_caller_identity.current.user_id}"
}

module "s3-bucket" {
  source  = "Smartbrood/s3-bucket/aws"
  version = "0.7.0"

  aws_account_id = "460402331925"
  aws_username   = "root"
  s3_fqdn        = "test-ri-audit"
}

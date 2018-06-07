// environment route53 zone
output "aws_audit_lambda_common_role_arn" {
  value = "${aws_iam_role.audit_lambda_common_role.arn}"
}

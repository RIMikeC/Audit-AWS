resource "aws_iam_role" "audit_lambda_common_role" {
  name = "actor_lambda_common_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "audit_lambda_common_role_policy" {
  name   = "audit_lambda_common_role"
  role   = "${aws_iam_role.audit_lambda_common_role.id}"
  policy = "${data.aws_iam_policy_document.audit_lambda_common_policy_document.json}"
}

data "aws_iam_policy_document" "audit_lambda_common_policy_document" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "ec2:CreateNetworkInterface",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DeleteNetworkInterface",
      "sns:Publish",
      "cloudwatch:*",
      "ce:GetCostAndUsage",
      "events:EnableRule",
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "audit_lambda_common_policy" {
  name   = "audit_lambda_common_policy"
  policy = "${data.aws_iam_policy_document.audit_lambda_common_policy_document.json}"
}

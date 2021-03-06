# AWS audit lambda 

# by mikec

# June 2018

resource "aws_iam_role" "audit_lambda" {
  name = "audit_lambda_role"

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

resource "aws_iam_role_policy" "audit_lambda_role_policy" {
  name   = "audit_lambda_common_role"
  role   = "${aws_iam_role.audit_lambda.id}"
  policy = "${data.aws_iam_policy_document.audit_lambda_policy_document.json}"
}

data "aws_iam_policy_document" "audit_lambda_policy_document" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "events:EnableRule",
      "autoscaling:DescribeAutoScalingGroups",
      "s3:*",
      "ec2:DescribeInstances",
      "ec2:DescribeRouteTables",
      "ec2:DescribeVpcs",
      "ec2:DescribeSubnets",
      "ec2:DescribeInternetGateways",
      "ec2:DescribeTags",
      "ec2:DescribeVpcPeeringConnections",
      "lambda:ListFunctions",
      "ecs:ListClusters",
      "kinesis:ListStreams",
      "rds:DescribeDBClusters",
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "audit_lambda_policy" {
  name   = "audit_lambda_common_policy"
  policy = "${data.aws_iam_policy_document.audit_lambda_policy_document.json}"
}

data "archive_file" "lambda_audit_zip" {
  type        = "zip"
  source_dir  = "${path.module}/source"
  output_path = "${path.module}/audit.zip"
}

resource "aws_lambda_function" "audit" {
  function_name    = "Audit-AWS"
  filename         = "${path.module}/audit.zip"
  source_code_hash = "${data.archive_file.lambda_audit_zip.output_base64sha256}"
  description      = "audit AWS"
  handler          = "audit_aws.lambda_handler"
  memory_size      = "128"
  timeout          = "10"
  role             = "${aws_iam_role.audit_lambda.arn}"
  runtime          = "python3.6"

  environment = {
    variables = {
      REGION = "eu-west-1"
    }
  }
}

# Create a new schedule to invoke the lambda

resource "aws_cloudwatch_event_rule" "audit_schedule" {
  name                = "audit_schedule"
  description         = "Periodically invokes audit"
  schedule_expression = "${var.audit_schedule}"
  is_enabled          = false
  depends_on          = ["aws_lambda_function.audit"]
}

resource "aws_cloudwatch_event_target" "audit" {
  rule = "${aws_cloudwatch_event_rule.audit_schedule.name}"
  arn  = "${aws_lambda_function.audit.arn}"
}

# Allow Cloudwatch to call the lambda function

resource "aws_lambda_permission" "allow_cloudwatch_to_call_audit" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.audit.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.audit_schedule.arn}"
}

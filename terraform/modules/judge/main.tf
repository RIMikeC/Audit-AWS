
resource "aws_iam_role" "aws_game" {
  name = "judge_lambda_role"

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

resource "aws_iam_role_policy" "aws_game_role_policy" {
  name   = "aws_game_role"
  role   = "${aws_iam_role.aws_game.id}"
  policy = "${data.aws_iam_policy_document.aws_game_policy_document.json}"
}

data "aws_iam_policy_document" "aws_game_policy_document" {
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

resource "aws_iam_policy" "aws_game_lambda_policy" {
  name   = "judge_lambda_policy"
  policy = "${data.aws_iam_policy_document.aws_game_policy_document.json}"
}

data "archive_file" "lambda_audit_zip" {
  type        = "zip"
  source_dir  = "${path.module}/source"
  output_path = "${path.module}/audit.zip"
}

resource "aws_lambda_function" "judge" {
  function_name    = "judge"
  filename         = "${path.module}/audit.zip"
  source_code_hash = "${data.archive_file.lambda_audit_zip.output_base64sha256}"
  description      = "Judge for the AWS Game"
  handler          = "judge.lambda_handler"
  memory_size      = "256"
  timeout          = "20"
  role             = "${aws_iam_role.aws_game.arn}"
  runtime          = "python3.6"

  environment = {
    variables = {
      REGION = "eu-west-1"
    }
  }
}

data "aws_s3_bucket" "selected" {
  bucket = "${var.bucket_name}"
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.judge.arn}"
  principal     = "s3.amazonaws.com"
  source_arn    = "${data.aws_s3_bucket.selected.arn}"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = "${data.aws_s3_bucket.selected.id}"

  lambda_function {
    lambda_function_arn = "${aws_lambda_function.judge.arn}"
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "audit/"
    filter_suffix       = ".json"
  }
}

data "archive_file" "lambda_audit_zip" {
  type        = "zip"
  source_dir  = "${path.module}/source"
  output_path = "${path.module}/audit.zip"
}

resource "aws_lambda_function" "audit" {
  function_name    = "Audit-AWS"
  filename         = "${path.module}/audit.zip"
  source_code_hash = "${data.archive_file.lambda_audit_zip.output_base64sha256}"
  description      = "Dump AWS charges into CW"
  handler          = "audit_aws.lambda_handler"
  memory_size      = "256"
  timeout          = "20"
  role             = "${var.lambda_role}"
  runtime          = "python3.6"

  environment = {
    variables = {
      REGION = "eu-west-1"
    }
  }
}

# Create a new schedule to run it at 8am

resource "aws_cloudwatch_event_rule" "audit_schedule" {
  name                = "audit_schedule"
  description         = "Periodically invokes audit"
  schedule_expression = "cron(0 8 * * ? *)"
  is_enabled          = true
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

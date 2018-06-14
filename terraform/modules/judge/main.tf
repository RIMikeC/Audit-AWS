data "archive_file" "lambda_audit_zip" {
  type        = "zip"
  source_dir  = "${path.module}/source"
  output_path = "${path.module}/audit.zip"
}

resource "aws_lambda_function" "judge" {
  function_name    = "judge"
  filename         = "${path.module}/judge.zip"
  source_code_hash = "${data.archive_file.lambda_audit_zip.output_base64sha256}"
  description      = "Judge for the AWS Game"
  handler          = "judge.lambda_handler"
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


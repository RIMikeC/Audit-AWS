// This should be converted into an invocation of a Registry Module, once it exists and is stable //
// It should also be moved, maybe to core-infrastructure-terraform/modules/something/  //

resource "aws_s3_bucket" "audit_storage" {
  bucket        = "${var.s3_bucket_name}"
  request_payer = "Requester"
  policy        = "${data.aws_iam_policy_document.s3_bucket.json}"
  tags          = "${var.bucket_tags}"

  versioning {
    enabled = false
  }

  lifecycle_rule {
    enabled = true

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "s3_bucket" {
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["arn:aws:s3:::${var.s3_bucket_name}/audit/*"]

    principals = {
      type        = "AWS"
      identifiers = ["${formatlist("arn:aws:iam::%s:root", compact(concat(var.contestants, list(data.aws_caller_identity.current.account_id))))}"]
    }
  }
}

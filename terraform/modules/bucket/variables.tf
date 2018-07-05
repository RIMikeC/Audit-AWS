variable "contestants" {
  type        = "list"
  description = "Contestants IDs"
  default     = ["666469064441","460402331925"]
}

variable "s3_bucket_name" {
  type        = "string"
  description = "storage for the AWS audit"
  default     = "std-ri-aws-audit"
}

variable "bucket_tags" {
  type        = "map"
  description = "Tags to attach to the bucket"

  default {
    Name           = "AWS Audit"
    environment    = "production"
    project_name   = "AWS Audit"
    programme      = "AWS Audit"
    product        = "AWS Audit"
    cost_centre    = "unknown"
    security_class = "public"
    terraform      = "true"
    repo           = "https://github.com/RIMikeC/Audit-AWS"
  }
}

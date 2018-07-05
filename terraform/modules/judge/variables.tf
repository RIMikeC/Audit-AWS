
variable "bucket_arn" {
  type        = "string"
  description = "Bucket in which the audit info is collected"
  default     = "arn:aws:s3:::ri-aws-audit"
}

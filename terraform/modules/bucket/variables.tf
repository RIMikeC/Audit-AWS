variable "contestants" {
  type        = "list"
  description = "Contestants IDs"
  default     = ["666469064441"]
}

variable "s3_bucket_name" {
  type        = "string"
  description = "storage for the AWS audit"
  default     = "ri-aws-audit"
}

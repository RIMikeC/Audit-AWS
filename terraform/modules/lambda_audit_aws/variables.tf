variable "audit_schedule" {
  default     = "cron(0,20,40 * * * ? *)"
  type        = "string"
  description = "Cron expression which shows when to invoke the audit lambda"
}

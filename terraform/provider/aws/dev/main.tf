provider "aws" {
  region = "eu-west-1"
}

// This should go into another account, maybe transit prod?

#module "buildabucket" {
#  source = "../../../modules/bucket"
#}

// This bit should go into shared_lambdas

module "invokeaudit" {
  source = "../../../modules/lambda_audit_aws"
}

// This bit should go into another account, maybe transit prod?


#module "goJudy" {
#  source = "../../../modules/judge"
#}


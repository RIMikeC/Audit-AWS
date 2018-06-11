provider "aws" {
  region = "eu-west-1"
}

module "game" {
  source = "../../bucket"
}

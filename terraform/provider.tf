terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region     = "ap-northeast-2"
  # Hard-coding credentials is not recommended
  # access_key = "XXXXXXXXXXXXXX"
  # secret_key = "XXXXXXXXXXXXXX"
}
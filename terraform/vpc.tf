provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_vpc" "girlsknight" {
  cidr_block = "172.36.0.0/16"
  tags = {
    "Name" = "girlsknight-vpc"
  }
}

output "vpc_girlknight" {
  value= aws_vpc.girlsknight
}
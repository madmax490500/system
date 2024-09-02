provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_vpc" "gk" {
  cidr_block = "172.36.0.0/16"
  tags = {
    "Name" = "gk-vpc"
  }
}

# 인터넷 게이트웨이 생성
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.gk.id

  tags = {
    "Name" = "gk-igw"
  }
}

# 서브넷 생성 (public subnet 예시)
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.gk.id
  cidr_block              = "172.36.10.0/24"
  availability_zone       = "ap-northeast-2a"
  
  tags = {
    "Name" = "gk-public-subnet"
  }
}

# 서브넷 생성 (DB public subnet 예시)
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.gk.id
  cidr_block              = "172.36.20.0/24"
  availability_zone       = "ap-northeast-2a"
  
  tags = {
    "Name" = "gk-DB public-subnet"
  }
}

# 라우팅 테이블 생성
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.gk.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    "Name" = "gk-public-rt"
  }
}

# 서브넷과 라우팅 테이블 연결
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

output "vpc_girlknight" {
  value = aws_vpc.gk
}

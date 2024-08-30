# RSA 알고리즘을 이용해 private 키 생성.
resource "tls_private_key" "pk" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# private 키를 가지고 keypair 파일 생성.
resource "aws_key_pair" "kp" {
  key_name   = "deleteme_keypair"
  public_key = tls_private_key.pk.public_key_openssh
}

# 키 파일을 생성하고 로컬에 다운로드.
resource "local_file" "ssh_key" {
  filename = "${aws_key_pair.kp.key_name}.pem"
  content = tls_private_key.pk.private_key_pem
}
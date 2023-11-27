terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

resource "tls_private_key" "my_ssh_key" {
  algorithm = "RSA"
}

resource "aws_key_pair" "my_key_pair" {
  key_name   = "iaac"
  public_key = tls_private_key.my_ssh_key.public_key_openssh
}

resource "aws_instance" "my_instance" {
  ami           = "ami-053b0d53c279acc90"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.my_key_pair.key_name
  vpc_security_group_ids = [aws_security_group.my_security_group.id]
  user_data = "${file("./scripts/deployment.sh")}"
  tags = {
    Name = "grupo13-iaac"
  }
}

resource "aws_eip" "my_eip" {
  instance = aws_instance.my_instance.id
}

resource "aws_security_group" "my_security_group" {
  name        = "my-security-group"
  description = "Security group for SSH access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

output "elastic_ip" {
  value = aws_eip.my_eip.public_ip
}

output "ssh_command" {
  value = "ssh -i ${aws_key_pair.my_key_pair.key_name}.pem ubuntu@${aws_eip.my_eip.public_ip}"
}


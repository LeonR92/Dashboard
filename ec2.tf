provider "aws" {
  region = "eu-central-1"
}

resource "aws_default_vpc" "default" {

}

resource "aws_security_group" "My_NSG" {
  name        = "My_NSG"
  description = "Allow SSH, HTTP, and TCP 3306 traffic"
  vpc_id      = aws_default_vpc.default.id

  # Ingress rules
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "example" {
  ami           = "ami-01342111f883d5e4e"
  instance_type = "t2.micro"
  key_name      = "perfect"

  vpc_security_group_ids = [aws_security_group.My_NSG.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              sudo systemctl enable docker
              sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
              EOF

  tags = {
    Name = "example-instance"
  }
}

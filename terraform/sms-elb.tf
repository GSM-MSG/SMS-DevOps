resource "aws_lb" "sms-alb" {
  name               = "sms-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.sms-alb-sg]
  subnets            = [for subnet in aws_subnet.public : subnet.id]

  enable_deletion_protection = false

  tags = {
    Environment = "production",
    Name = "sms-alb"
  }
}

resource "aws_security_group" "sms-alb-sg" {
    vpc_id = "${aws_vpc.sms-vpc.id}"

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
      from_port = 8080
      to_port = 8080
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
      from_port = 8090
      to_port = 8090
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
    }

    tags = {
        Name = "sms-alb-sg"
    }
}
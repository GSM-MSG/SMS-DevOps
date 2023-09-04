resource "aws_lb" "sms-alb" {
  name               = "sms-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = ["${aws_security_group.sms-alb-sg.id}"]
  subnets            = [
        "${aws_subnet.sms-public-subnet-2a.id}",
        "${aws_subnet.sms-public-subnet-2b.id}"
  ]

  enable_deletion_protection = false

  tags = {
    Environment = "production",
    Name = "sms-alb"
  }
}

resource "aws_lb_listener" "sms-alb-listener" {
  load_balancer_arn = aws_lb.sms-alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.sms-tg.arn
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


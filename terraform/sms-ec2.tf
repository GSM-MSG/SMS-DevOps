# Create EC2
## Create Bastion + Nat Instance
resource "aws_instance" "sms-bastion" {
    ami = "ami-04cebc8d6c4f297a3"
    instance_type =  "t2.nano"
    subnet_id = "${aws_subnet.sms-public-subnet-2a.id}"
    vpc_security_group_ids = [aws_security_group.sms-bastion-sg.id]
    key_name = "sms-key"

    tags = {
        Name = "sms-bastion"
    }
}

resource "aws_instance" "sms-main-server" {
    ami = "ami-04cebc8d6c4f297a3"
    instance_type = "t3.medium"
    subnet_id = "${aws_subnet.sms-private-subnet-2a.id}"
    vpc_security_group_ids = [aws_security_group.sms-main-server-sg.id]
    key_name = "sms-key"
    associate_public_ip_address = false
    source_dest_check = false

    tags = {
        Name = "sms-main-server"
    }
}   

# Create SG
## Create Bastion SG
resource "aws_security_group" "sms-bastion-sg" {
    vpc_id = "${aws_vpc.sms-vpc.id}"

    ingress {
        from_port = 22
        to_port = 22
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
        Name = "sms-sg"
    }
}

## Create Main Server SG
resource "aws_security_group" "sms-main-server-sg" {
    vpc_id = "${aws_vpc.sms-vpc.id}"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        security_groups = [aws_security_group.sms-bastion-sg.id]
    }

    ingress{
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    ingress{
        from_port = 6379
        to_port = 6379
        protocol = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    ingress{
        from_port = 587
        to_port = 587
        protocol = "tcp"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    egress {
        from_port       = 0
        to_port         = 0
        protocol        = "-1"
        cidr_blocks     = ["0.0.0.0/0"]
    }

    tags = {
        Name = "sms-main-server-sg"
    }
}
data "aws_availability_zones" "available" {
    state = "available"
}

# Create VPC
resource "aws_vpc" "sms-vpc"{
    cidr_block = "192.168.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
    instance_tenancy = "default"

    tags = {
        Name = "sms-vpc"
    }
}

## Create Public Subnet
resource "aws_subnet" "sms-public-subnet-2a" {
    vpc_id = aws_vpc.sms-vpc.id
    cidr_block = "192.168.0.0/20"
    map_public_ip_on_launch = true
    availability_zone = data.aws_availability_zones.available.names[0]
    tags = {
        "Name" = "sms-public-subnet-2a"
    }
}

resource "aws_subnet" "sms-public-subnet-2b" {
    vpc_id = aws_vpc.sms-vpc.id
    cidr_block = "192.168.32.0/20"
    map_public_ip_on_launch = true
    availability_zone = data.aws_availability_zones.available.names[1]
    tags = {
        "Name" = "sms-public-subnet-2b"
    }
}

## Create Subnet Private
resource "aws_subnet" "sms-private-subnet-2a" {
    vpc_id = aws_vpc.sms-vpc.id
    cidr_block = "192.168.16.0/20"
    map_public_ip_on_launch = false
    availability_zone = data.aws_availability_zones.available.names[0]
    tags = {
        "Name" = "sms-private-subnet-2a"
    }
}

resource "aws_subnet" "sms-private-subnet-2b" {
    vpc_id = aws_vpc.sms-vpc.id
    cidr_block = "192.168.48.0/20"
    map_public_ip_on_launch = false
    availability_zone = data.aws_availability_zones.available.names[1]
    tags = {
        "Name" = "sms-private-subnet-2b"
    }
}

# Create IGW
resource "aws_internet_gateway" "sms-igw" {
    vpc_id = aws_vpc.sms-vpc.id
    tags = {
        Name = "sms-igw"
    }
}

# Create Nat
resource "aws_nat_gateway" "sms-nat" {
    subnet_id = aws_subnet.sms-public-subnet-2a.id

    tags = {
        Name = "sms-nat"
    }
}


# Create RTB 
## Create Public RTB
resource "aws_route_table" "sms-public-rtb" {
    vpc_id = aws_vpc.sms-vpc.id

    tags = {
        Name = "sms-public-rtb"
    }
}

## Create Private RTB
resource "aws_route_table" "sms-private-rtb" {
    vpc_id = aws_vpc.sms-vpc.id

    tags = {
        Name = "sms-private-rtb"
    }
}

# Subnet Register RTB #
## Public Subnet Register RTB ## 
resource "aws_route_table_association" "sms-public-rt-association-1" {
    subnet_id = aws_subnet.sms-public-subnet-2a.id
    route_table_id = aws_route_table.sms-public-rtb.id
}

resource "aws_route_table_association" "sms-public-rt-association-2" {
    subnet_id = aws_subnet.sms-public-subnet-2b.id
    route_table_id = aws_route_table.sms-public-rtb.id
}

## Private Subnet Register RTB ## 
resource "aws_route_table_association" "sms-private-rt-association-1" {
    subnet_id = aws_subnet.sms-private-subnet-2a.id
    route_table_id = aws_route_table.sms-private-rtb.id
}

resource "aws_route_table_association" "sms-private-rt-association-2" {
    subnet_id = aws_subnet.sms-private-subnet-2b.id
    route_table_id = aws_route_table.sms-private-rtb.id
}

## IGW Register RTB ##
resource "aws_route" "public-rt-igw" {
    route_table_id = aws_route_table.sms-public-rtb.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.sms-igw.id
}

## Nat Register RTB
resource "aws_route" "private-rt-nat" {
    route_table_id = aws_route_table.sms-private-rtb.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.sms-nat.id
}
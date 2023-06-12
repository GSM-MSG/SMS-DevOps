terraform {
    backend "s3" {
        bucket = "devops-tf-1124sd25"
        key = "terraform/terraform.tfstate"
        region = "ap-northeast-2"
        encrypt = true
        dynamodb_table = "terrafomr-lock"
    }
}

provider "aws" {
    region = "ap-northeast-2" 
    version = "~> 2.49.0" 
}

resource "aws_s3_bucket" "devops-terraform-archive" {
    bucket = "devops-tf-1124sd25"

    versioning {
        enabled = true
    }
}

resource "aws_dynamodb_table" "terraform_state_lock" {
    name = "terraform-lock"
    hash_key = "LockID"
    billing_mode = "PAY_PER_REQUEST"

    attrbute {
        name = "LockID"
        type = "S"
    }
}
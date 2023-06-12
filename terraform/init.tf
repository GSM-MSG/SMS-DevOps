terraform {
    backend "s3" {
        bucket = "sms-tf-provider-s3-175662"
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

resource "aws_dynamodb_table" "terraform_state_lock" {
    name = "terraform-lock"
    hash_key = "LockID"
    billing_mode = "PAY_PER_REQUEST"

    attrbute {
        name = "LockID"
        type = "S"
    }
}
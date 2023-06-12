terraform {
    backend "s3" {
        bucket = "sms-tf-provider-s3-175662"
        key = "terraform/terraform.tfstate"
        region = "ap-northeast-2"
        encrypt = true
        dynamodb_table = "terraform-lock"
    }
}

provider "aws" {
    region = "ap-northeast-2" 
    version = "~> 2.49.0" 
}
# Var
variable "code_pipeline_bucekt" {
    type = string
}

# Create S3 Bucket
resource "aws_s3_bucket" "sms-s3-buckets" {
    bucket = var.code_pipeline_bucekt
}
resource "aws_dynamodb_table" "lockid-table"{
    name           = "LockID"
    billing_mode   = "PROVISIONED"
    read_capacity  = 10
    write_capacity = 10
    hash_key       = "terrafomr-lock"
}
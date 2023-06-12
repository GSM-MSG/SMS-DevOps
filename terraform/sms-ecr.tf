resource "aws_ecr_repository" "sms-ecr" {
    name = "sms-ecr"
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
        scan_on_push = true
    }
}
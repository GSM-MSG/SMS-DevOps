resource "aws_ecr_repository" "sms-ecr-repo" {
    name = "sms-ecr-repo"
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
        scan_on_push = true
    }
}

resource "aws_ecr_repository" "sms-nyopa-repo" {
    name = "sms-nyopa-repo"
    image_tag_mutability = "MUTABLE"

    image_scanning_configuration {
        scan_on_push = true
    }
}
data "aws_iam_policy_document" "assume_role" {
    statement {
        effect = "Allow"

    principals {
        type        = "Service"
        identifiers = ["codedeploy.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
    }
}

resource "aws_iam_role" "codedeploy-role" {
    name               = "codedeploy-role"
    assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "AWSCodeDeployRole" {
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole"
    role       = aws_iam_role.codedeploy-role.name
}
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

resource "aws_codedeploy_app" "codedeploy-application" {
    compute_platform = "Server"
    name             = "codedeploy-application"
}

resource "aws_codedeploy_deployment_group" "codedeploy-group" {
    app_name = aws_codedeploy_app.codedeploy-application.name
    deployment_group_name = "codedeploy-group"
    service_role_arn = aws_iam_role.codedeploy-role.arn
}
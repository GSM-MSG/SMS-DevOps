# ssm, cloudwatch agent를 허용하는 역할 생성
resource "aws_iam_role" "EC2InstacneToSSMandCloudwatchAgent" {
  name = "test_EC2InstacneToSSMandCloudwatchAgent"
  path = "/"
  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Principal" : {
            "Service" : "ec2.amazonaws.com"
          },
          "Action" : "sts:AssumeRole"
        }
      ]
    }
  )
}


# 역할을 ec2 인스턴스에 연결하기 위해 인스턴스 프로파일 생성
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.EC2InstacneToSSMandCloudwatchAgent.name
}

# ssm 접근 허용 정책(EC2 용)
data "aws_iam_policy" "AmazonSSMManagedInstanceCore" {
  name = "AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "AmazonSSMManagedInstanceCore" {
  role       = aws_iam_role.EC2InstacneToSSMandCloudwatchAgent.name
  policy_arn = data.aws_iam_policy.AmazonSSMManagedInstanceCore.arn
}

# cloudwatch agent 허용 정책(EC2 용)
data "aws_iam_policy" "CloudWatchAgentServerPolicy" {
  name = "CloudWatchAgentServerPolicy"
}

resource "aws_iam_role_policy_attachment" "CloudWatchAgentServerPolicy" {
  role       = aws_iam_role.EC2InstacneToSSMandCloudwatchAgent.name
  policy_arn = data.aws_iam_policy.CloudWatchAgentServerPolicy.arn
}
resource "aws_lb_target_group" "sms-tg" {
    name     = "sms-tg"
    port     = 80
    protocol = "HTTP"
    vpc_id   = aws_vpc.sms-vpc.id
}

resource "aws_lb_target_group_attachment" "test" {
    target_group_arn = aws_lb_target_group.sms-tg.arn
    target_id        = aws_instance.sms-main-server.id
    port             = 8090
}

resource "aws_lb_target_group_attachment" "test" {
    target_group_arn = aws_lb_target_group.sms-tg.arn
    target_id        = aws_instance.sms-main-server.id
    port             = 8080
}
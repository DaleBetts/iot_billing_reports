data "aws_caller_identity" "current" {}

resource "aws_iam_role" "s3_billing_report_role" {
  name = "s3_billing_report_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "s3_billing_report_policy" {
  name = "s3_billing_report_policy"
  role = "${aws_iam_role.s3_billing_report_role.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:List*",
                "s3:Get*",
                "s3:HeadBucket",
                "logs:Put*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:eu-west-1:${data.aws_caller_identity.current.account_id}:${aws_sns_topic.bill_updates.name}"
        }
    ]
}
EOF
}

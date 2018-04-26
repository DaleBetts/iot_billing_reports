data "archive_file" "dotfiles" {
  type        = "zip"
  source_dir  = "../../../lambda/src/s3_billing_report"
  output_path = "../../../lambda/files/s3-billing-report.zip"
}

resource "aws_lambda_function" "lambda_s3_billing_report" {
  filename      = "../../../lambda/files/s3-billing-report.zip"
  function_name = "s3-billing-report"
  handler       = "s3-billing-report.lambda_handler"
  timeout       = 60
  runtime       = "python2.7"
  role          = "${aws_iam_role.s3_billing_report_role.arn}"
}

resource "aws_sns_topic" "bill_updates" {
  name = "bill-updates-topic"
}

data "template_file" "init" {
  template = "${path.module}/vars.ini.tpl"

  vars {
    sns_arn = "${aws_sns_topic.bill_updates.arn}"
  }
}

resource "local_file" "lambda_config" {
    content     = "${data.template_file.init.rendered}"
    filename = "../../../lambda/src/s3_billing_report/vars.ini"
}

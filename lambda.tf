data "archive_file" "dotfiles" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/files/s3-billing-report.zip"
}

resource "aws_lambda_function" "lambda_s3_billing_report" {
  s3_bucket     = "${var.lambda_s3_bucket}"
  s3_key        = "${var.lambda_s3_key}"
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
  template = "${file("${path.module}/vars.ini.tpl")}"

  vars {
    sns_arn = "${aws_sns_topic.bill_updates.arn}"
    aws_account_id = "${data.aws_caller_identity.current.account_id}"
  }
}

resource "local_file" "lambda_config" {
  content  = "${data.template_file.init.rendered}"
  filename = "${path.module}/src/vars.ini"
}

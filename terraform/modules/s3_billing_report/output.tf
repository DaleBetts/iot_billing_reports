output "sns_arn" {
  value = "${aws_sns_topic.bill_updates.arn}"
}

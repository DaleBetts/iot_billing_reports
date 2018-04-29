[s3]
report_bucket = your-bill-s3-bucket 
[regions]
region_list = eu-west-1
[config]
custom_prefix = ${aws_account_id}-aws-billing-detailed-line-items-with-reso
custom_suffix = csv.zip
sns_arn = ${sns_arn} 

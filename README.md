# IOT Billing Reports

## What is this project?

This is my first IOT project as I recently purchased one of the Amazon IOT buttons.

The goal that I wish to accomplish here is to get instant billing feedback from AWS, as I'm notorious for leaving pesky resources such as snapshots, volumes, etc lying around after some personal development tasks.

AWS only provide hourly billing, but this is ok for what I need. The Lambda will read from a given s3 bucket, parse the latest reports and send via SMS (default). This can be configured to be any SNS protocol however.

## Pre-requisites

To use this repo you first of all need to configure your "Billing & Cost Management Dashboard" -> Preferences -> "Receive Billing Reports" and save the hourly reports to your own S3 bucket.

Remember to enable the sample s3 bucket policy and validate that these reports are being published to your bucket hourly.

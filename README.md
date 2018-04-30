# IOT Button - Send me my AWS Bill

## What is this project?

This is my first IOT project as I recently purchased an Amazon IOT button.

The goal here was to get instant billing feedback from AWS. As a serial offender for leaving pesky resources such as snapshots, volumes and ec2 instances etc lying around in my development AWS account, I needed something to keep track of these costs.

AWS provide detailed billing which is delivered numerous times a day to an S3 bucket. The Lambda finds the latest bill, parses the CSV and sends via SNS. Currently the code supports email and SMS (in SMS supported regions, I tend to use eu-west-1)

## Pre-requisites

To use this repo you first of all need to configure your "Billing & Cost Management Dashboard" -> Preferences -> "Receive Billing Reports" and save the hourly reports to your own S3 bucket.

Remember to enable the sample s3 bucket policy and validate that these reports are being published to your bucket hourly.

## Getting Started

The Lambda source code needs to be compiled into a zip and has dependencies that won't work out of the box with core Lambda Python 2.7. Lambda run on EC2 via Amazon Linux and thus the compiled source code should be built on the same architecture. I tend to spawn an EC2 running Amazon Linux 2 to compile these dependencies.

```
pip install numpy
pip install pandas
pip install pytz

python
import pandas
pandas.__file__

```

Make a note of where your compiled code is stored and copy these directories to src

```
# clone the repo
terraform init
terraform plan
terraform apply
```

Copy the compiled zip in files/s3-billing-report.zip to s3 in the location you entered during `terraform apply`

You should now be able to test the lambda function successfully. Once confirmed, simply assign your IOT button to the Lambda.

You will need to subscribe to your SNS topic which is provided as an output from terraform. Run `terraform refresh` as a reminder for the ARN or use the AWS console.


## Contributions and Feedback

Feel free to recommend improvements or contribute via a PR. 


# Thanks and References

Thanks to this blog for providing useful lookup code for s3 files:

https://alexwlchan.net/2018/01/listing-s3-keys-redux/




terraform {
  backend "s3" {
    bucket = "dataqube-terraform-remote-state"
    key    = "sandbox/iot_terraform.tfstate"
    region = "eu-west-2"
  }
}

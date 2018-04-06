import boto3
import ConfigParser
import botocore
import datetime
import re
import collections

config = ConfigParser.RawConfigParser()
config.read('./vars.ini')

print('Loading IOT Billing Report Function')

def lambda_handler(event, context):
    regionsStrg = config.get('regions', 'regionList')
    regionsList = regionsStrg.split(',')
    EC2_INSTANCE_TAG = config.get('s3', 'reportBucket')
    ec2_instance_tags = EC2_INSTANCE_TAG.split(',')

lambda_handler('test','test')

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
    s3Bucket = config.get('s3', 'reportBucket')
    print("something")
        


#lambda_handler('test','test')

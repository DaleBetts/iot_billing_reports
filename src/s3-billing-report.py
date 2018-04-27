import boto3
import ConfigParser
import botocore
import pandas as pd
import zipfile
import io
import json

config = ConfigParser.RawConfigParser()
config.read('./vars.ini')

print('Loading IOT Billing Report Function')

def lambda_handler(event, context):
    regions_strg = config.get('regions', 'region_list')
    regions_list = regions_strg.split(',')
    s3_bucket = config.get('s3', 'report_bucket')
    custom_prefix = config.get('config', 'custom_prefix').strip()
    custom_suffix = config.get('config', 'custom_suffix').strip()
    sns_arn = config.get('config', 'sns_arn').strip()

    for key in get_matching_s3_keys(bucket=s3_bucket,prefix=custom_prefix, suffix=custom_suffix):
        client = boto3.client('s3')
        obj = client.get_object(Bucket=s3_bucket, Key=key)
        buffer = io.BytesIO(obj["Body"].read())
        zip_file = zipfile.ZipFile(buffer,'r')
        for name_of_zipfile in zip_file.namelist():
          df = pd.read_csv(zip_file.open(name_of_zipfile))
          #print(df["Cost"].iloc[-2])
          bill = "$" + str(df["Cost"].iloc[-2])

    message = {"bill": bill}
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=sns_arn,
        Message=json.dumps({'default': json.dumps(message),
                            'sms': bill,
                            'email': bill}),
        Subject="Your Latest AWS Bill is: " + bill,
        MessageStructure='json'
    )



def get_matching_s3_objects(bucket, prefix='', suffix=''):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)

        try:
            contents = resp['Contents']
        except KeyError:
            return

        for obj in contents:
            key = obj['Key']
            if key.endswith(suffix):
                yield obj

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break


def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj['Key']


#lambda_handler('test','test')

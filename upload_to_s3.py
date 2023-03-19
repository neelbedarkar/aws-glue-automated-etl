import os
import boto3
from botocore.client import ClientError
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

bucket_name = config.get('S3', 'bucket_name')
file_path = config.get('S3', 'file_to_upload')
file_object_name = config.get('S3', 's3_object_name')

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


print(bucket_name)


def create_bucket():
    response = s3.create_bucket(
        Bucket=bucket_name,
        ACL='private'
    )
    print(response)


def search_bucket():
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        return 0  # replace this with some other tristate return or update the logic.
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print("Bucket Not Found")
            return 1
        elif error_code == 403:
            print("No access to bucket")
            return 2
        else:
            raise Exception("Bad response")


def s3_upload_file(object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(response)
    except ClientError as e:
        print(e)
        return False
    return True


bucket_found_code = search_bucket()
if bucket_found_code == 1:
    create_bucket()
elif bucket_found_code == 0:
    print("bucket is found and can be accessed")
else:
    raise Exception("Bucket exists and cannot be accessed. Check name of the bucket in the config file")


s3_upload_file(file_object_name)

import boto3
from botocore.client import ClientError

s3 = boto3.resource('s3')

with open("config.txt", "r") as f:
    bucket_name = f.readline().strip("\n")

if not bucket_name:
    print("Could not read file. Please create it and add bucket name")
    raise SystemExit

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
        return 0
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


bucket_found_code = search_bucket()

if bucket_found_code == 1:
    create_bucket()
elif bucket_found_code == 0:
    print("bucket is found and can be accessed")
else:
    raise Exception("Bucket exists and cannot be accessed. Check name of the bucket in the config file")












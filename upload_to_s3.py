import boto3
s3 = boto3.resource('s3')

with open("bucket_name.txt", "r") as f:
    bucket_name = f.readline().strip("\n")

if not bucket_name:
    print("Could not read file. Please create it and bucket name")
    raise SystemExit

print(bucket_name)

bucket_found = False
for bucket in s3.buckets.all():
    if bucket.name == bucket_name:
        bucket_found = True

if not bucket_found:
    response = s3.create_bucket(
            Bucket=bucket_name,
         CreateBucketConfiguration={
            'LocationConstraint': 'us-east-2',
        },
        ACL='private'
    )
    print(response)








import boto3
s3 = boto3.resource('s3')
bucket_name = 'aws-glue-example-bucket-3.18.2023'

response = s3.create_bucket(
        Bucket=bucket_name,
     CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2',
    },
    ACL='private'
)
print(response)

for bucket in s3.buckets.all():
    print(bucket.name)







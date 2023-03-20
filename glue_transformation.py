import boto3
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

s3_link = config.get('S3', 's3_link')
s3_object_name = config.get('S3', 's3_object_name')


client = boto3.client('glue', region_name="us-east-2")

response = client.create_crawler(
    Name='S3Crawler',
    Role='GlueToS3',
    DatabaseName='S3CrawlerHOC',
    Targets={
        'S3Targets': [
            {
                'Path': s3_link + s3_object_name,
                'SampleSize': 2
            },
            {
                'Path':  s3_link,
                'SampleSize': 2
            },
        ]
    },
    Schedule='cron(15 12 * * ? *)',
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
    },
    RecrawlPolicy={
        'RecrawlBehavior': 'CRAWL_EVERYTHING'
    },
    LineageConfiguration={
        'CrawlerLineageSettings': 'DISABLE'
    }
)
print(json.dumps(response, indent=4, sort_keys=True, default=str))

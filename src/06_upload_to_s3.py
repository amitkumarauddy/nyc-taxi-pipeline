import boto3
import os

print("Connecting to local AWS S3...")

# 1. Configure the AWS Client to target your Docker container
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

bucket_name = 'taxi-data-lake'
file_path = 'data/gold/daily_revenue_metrics.parquet'
s3_key = 'gold/daily_revenue_metrics.parquet'

# 2. Execute the Cloud Upload
print(f"Uploading Medallion metrics to s3://{bucket_name}/{s3_key}...")

try:
    s3.upload_file(file_path, bucket_name, s3_key)
    print("Upload complete! The Gold dataset is securely stored in the Data Lake.")
except Exception as e:
    print(f"Upload failed: {e}")

import boto3

print("Connecting to local AWS S3...")

# Try multiple endpoint URLs for compatibility
endpoints = [
    'http://host.docker.internal:4566',  # Docker Desktop
    'http://mock-aws-cloud:4566',         # Docker network (container name)
    'http://localstack:4566',             # Docker network (service name)
    'http://localhost:4566'                # Fallback
]

s3 = None
endpoint_used = None

for endpoint in endpoints:
    try:
        print(f"Trying endpoint: {endpoint}")
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        # Test connection by listing buckets
        s3_client.list_buckets()
        s3 = s3_client
        endpoint_used = endpoint
        print(f"✓ Connected successfully to {endpoint}")
        break
    except Exception as e:
        print(f"✗ Failed to connect to {endpoint}: {e}")
        continue

if s3 is None:
    print("ERROR: Could not connect to LocalStack on any endpoint")
    print("Make sure LocalStack is running: docker compose up -d")
    exit(1)

bucket_name = 'taxi-data-lake'
file_path = 'data/gold/daily_revenue_metrics.parquet'
s3_key = 'gold/daily_revenue_metrics.parquet'

# 2. Ensure bucket exists
print(f"\nEnsuring bucket '{bucket_name}' exists...")
try:
    s3.head_bucket(Bucket=bucket_name)
    print(f"✓ Bucket '{bucket_name}' already exists")
except s3.exceptions.NoSuchBucket:
    print(f"Creating bucket '{bucket_name}'...")
    s3.create_bucket(Bucket=bucket_name)
    print(f"✓ Bucket '{bucket_name}' created")
except Exception as e:
    print(f"✗ Error checking/creating bucket: {e}")
    exit(1)

# 3. Execute the Cloud Upload
print(f"\nUploading Medallion metrics to s3://{bucket_name}/{s3_key}...")

try:
    s3.upload_file(file_path, bucket_name, s3_key)
    print("✓ Upload complete! The Gold dataset is securely stored in the Data Lake.")
except FileNotFoundError:
    print(f"✗ Error: Could not find file '{file_path}'")
except Exception as e:
    print(f"✗ Upload failed: {e}")

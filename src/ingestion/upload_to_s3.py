"""
upload_to_s3.py

Downloads the Credit Card Fraud Detection dataset (via kagglehub)
and uploads the raw CSV to the S3 raw/ layer.
"""

import os
import boto3
import kagglehub
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

print("Downloading dataset from Kaggle...")
dataset_path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
print(f"Downloaded to: {dataset_path}")

csv_file = os.path.join(dataset_path, "creditcard.csv")

print("Connecting to S3...")
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

print(f"Uploading to s3://{S3_BUCKET}/raw/creditcard.csv ...")
s3.upload_file(csv_file, S3_BUCKET, "raw/creditcard.csv")

print("Done. Raw data is now in S3.")
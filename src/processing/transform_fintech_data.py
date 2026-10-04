"""
transform_fintech_data.py

Reads the raw credit card transaction CSV from S3, cleans it,
converts to Parquet, and writes it back to S3 processed/ layer,
partitioned by transaction_day.
"""

import os
import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

RAW_KEY = "raw/creditcard.csv"
LOCAL_RAW = "data_raw_creditcard.csv"
LOCAL_PROCESSED_DIR = "processed_output"

print(f"Downloading s3://{S3_BUCKET}/{RAW_KEY} ...")
s3.download_file(S3_BUCKET, RAW_KEY, LOCAL_RAW)

print("Reading CSV...")
df = pd.read_csv(LOCAL_RAW)
print(f"Raw shape: {df.shape}")

# --- Column standardisation ---
df.columns = [c.strip().lower() for c in df.columns]

# --- Missing-value handling ---
missing_before = df.isnull().sum().sum()
df = df.dropna()
print(f"Missing cells found: {missing_before}. Rows after dropna: {df.shape[0]}")

# --- Duplicate check ---
dupes = df.duplicated().sum()
df = df.drop_duplicates()
print(f"Duplicate rows dropped: {dupes}. Rows remaining: {df.shape[0]}")

# --- Type conversion ---
df["class"] = df["class"].astype(int)
df["amount"] = df["amount"].astype(float)
df["time"] = df["time"].astype(float)

# --- Derived partition column ---
# 'time' = seconds elapsed since the first transaction in the dataset
df["transaction_day"] = (df["time"] // 86400).astype(int)

print("Writing partitioned Parquet locally...")
df.to_parquet(
    LOCAL_PROCESSED_DIR,
    engine="pyarrow",
    partition_cols=["transaction_day"],
    index=False,
)

print("Uploading partitioned Parquet files to S3 processed/ ...")
for root, _, files in os.walk(LOCAL_PROCESSED_DIR):
    for file in files:
        local_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_path, LOCAL_PROCESSED_DIR)
        s3_key = f"processed/{relative_path}".replace("\\", "/")
        s3.upload_file(local_path, S3_BUCKET, s3_key)
        print(f"  Uploaded {s3_key}")

print("Done. Processed data is now in S3 under processed/.")
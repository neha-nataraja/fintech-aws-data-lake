\# Fintech Transaction Data Lake (AWS)



A cloud-native data lake for credit card transaction data, built on AWS — S3, Glue Data Catalog, and Athena — demonstrating a modern serverless analytics pipeline from raw ingestion through partitioned, queryable Parquet.



\## Architecture



Public Transaction Data (Kaggle / ULB)

↓

Python Ingestion

↓

AWS S3 (raw/)

↓

Python Transformation

(clean, dedupe, type-cast, partition)

↓

AWS S3 (processed/) — Parquet, partitioned by transaction\_day

↓

AWS Glue Data Catalog

↓

Amazon Athena (SQL)

↓

Business Analytics





\## Dataset



\*\*Credit Card Fraud Detection\*\* dataset (ULB / Kaggle) — anonymized European credit card transactions from September 2013. 284,807 transactions, 31 columns (`Time`, 28 PCA-transformed features `V1`–`V28`, `Amount`, `Class`). No personally identifiable information is contained in the source data.



\## Pipeline



1\. \*\*Ingestion\*\* (`src/ingestion/upload\_to\_s3.py`) — downloads the dataset programmatically via the Kaggle API and uploads the raw CSV to S3 `raw/`

2\. \*\*Transformation\*\* (`src/processing/transform\_fintech\_data.py`) — reads the raw CSV, standardises column names, handles missing values, removes duplicates, converts to Parquet, and writes it to S3 `processed/`, partitioned by `transaction\_day` (derived from the `Time` field)

3\. \*\*Cataloging\*\* — an external table is defined directly via Athena DDL against the partitioned Parquet in `processed/`, with partitions registered via `MSCK REPAIR TABLE`

4\. \*\*Analytics\*\* — SQL queries run through Athena against the cataloged table



\## Business Questions Answered



\- \*\*What is the overall fraud rate?\*\* 0.17% (473 fraudulent transactions out of 283,726)

\- \*\*Do fraudulent transactions differ in value?\*\* Yes — fraudulent transactions average $123.87 vs. $88.41 for legitimate ones (≈40% higher)

\- \*\*Does fraud rate vary over time?\*\* Yes — 0.19% on day 1 vs. 0.14% on day 2 of the dataset window



\## Data Quality



\- \*\*1,081 duplicate rows\*\* identified and removed during transformation (283,726 clean rows remain)

\- Automated checks confirm: zero null values in critical columns (`amount`, `class`), zero negative transaction amounts, `class` constrained to valid values (0/1 only)



\## Tech Stack



Python · pandas · pyarrow · boto3 · AWS S3 · AWS Glue Data Catalog · Amazon Athena · Git



\## Project Status



\- \[x] MVP1 — S3 ingestion, scoped IAM access

\- \[x] MVP2 — Python transformation, Parquet conversion, partitioning

\- \[x] MVP3 — Glue Data Catalog table (defined via Athena DDL)

\- \[x] MVP4 — Analytical SQL queries

\- \[x] MVP5 — Data quality validation



\## Design Decisions



\- \*\*No EC2, RDS, or always-on compute\*\* — this project intentionally uses only serverless/on-demand services (S3, Athena) to stay cost-conscious in a personal AWS account

\- \*\*Least-privilege IAM\*\* — a scoped IAM user/policy restricts access to this project's S3 bucket only, rather than using broad account permissions

\- \*\*Partitioning by `transaction\_day`\*\* rather than an arbitrary column — chosen because it reflects how transaction data would realistically be partitioned and queried in production (time-based access patterns)



\## Why This Project



Building on `insurance-de-pipeline` (local pipeline: Python + PostgreSQL + dbt), this project demonstrates the same data engineering discipline — ingestion, transformation, data quality validation — applied to a cloud-native architecture (S3, Glue, Athena), extending into a second domain (fintech transaction data) to show both technical and domain breadth.



\## Reproducing This Project



git clone https://github.com/neha-nataraja/fintech-aws-data-lake.git

cd fintech-aws-data-lake

python -m venv .venv

.venv\\Scripts\\activate

pip install boto3 kagglehub pandas python-dotenv pyarrow



create a .env file with your own AWS credentials (see below)



python src/ingestion/upload\_to\_s3.py

python src/processing/transform\_fintech\_data.py



then run sql/create\_table.sql in the Athena query editor to catalog and query



`.env` format:



AWS\_ACCESS\_KEY\_ID=your\_access\_key

AWS\_SECRET\_ACCESS\_KEY=your\_secret\_key

AWS\_REGION=eu-north-1

S3\_BUCKET=your-bucket-name


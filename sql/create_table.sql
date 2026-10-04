-- create_table.sql
-- Defines the external table over the partitioned Parquet data in S3 processed/
-- Run this in the Athena query editor, with fintech_datalake_db selected as the database.

CREATE EXTERNAL TABLE IF NOT EXISTS fintech_datalake_db.processed_transactions (
  time DOUBLE,
  v1 DOUBLE, v2 DOUBLE, v3 DOUBLE, v4 DOUBLE, v5 DOUBLE,
  v6 DOUBLE, v7 DOUBLE, v8 DOUBLE, v9 DOUBLE, v10 DOUBLE,
  v11 DOUBLE, v12 DOUBLE, v13 DOUBLE, v14 DOUBLE, v15 DOUBLE,
  v16 DOUBLE, v17 DOUBLE, v18 DOUBLE, v19 DOUBLE, v20 DOUBLE,
  v21 DOUBLE, v22 DOUBLE, v23 DOUBLE, v24 DOUBLE, v25 DOUBLE,
  v26 DOUBLE, v27 DOUBLE, v28 DOUBLE,
  amount DOUBLE,
  class INT
)
PARTITIONED BY (transaction_day INT)
STORED AS PARQUET
LOCATION 's3://fintech-datalake-314201983350/processed/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- After creating the table, register existing partitions:
-- MSCK REPAIR TABLE fintech_datalake_db.processed_transactions;

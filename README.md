# nyc-taxi-pipeline

sudo apt install python3.12-venv

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

chmod +x src/00_download_year.sh

./src/00_download_year.sh

sudo apt install make

make help

 make run-all


(.venv) auddy@DGF3080:~/nyc-taxi-pipeline$ make run-all
Starting Pipeline Phase 1: Ingestion & Cleaning...
.venv/bin/python src/02_clean_and_combine.py
Initiating lazy scan of multiple months...
Total rows before cleaning: 48,722,602
Executing data quality filters...
Total rows after cleaning: 35,604,835
Bad records eliminated: 13,117,767

--- Clean Dataset Preview ---
shape: (5, 20)
┌──────────┬───────────────┬───────────────┬───────────────┬───┬──────────────┬───────────────┬─────────────┬──────────────┐
│ VendorID ┆ tpep_pickup_d ┆ tpep_dropoff_ ┆ passenger_cou ┆ … ┆ total_amount ┆ congestion_su ┆ Airport_fee ┆ cbd_congesti │
│ ---      ┆ atetime       ┆ datetime      ┆ nt            ┆   ┆ ---          ┆ rcharge       ┆ ---         ┆ on_fee       │
│ i32      ┆ ---           ┆ ---           ┆ ---           ┆   ┆ f64          ┆ ---           ┆ f64         ┆ ---          │
│          ┆ datetime[μs]  ┆ datetime[μs]  ┆ i64           ┆   ┆              ┆ f64           ┆             ┆ f64          │
╞══════════╪═══════════════╪═══════════════╪═══════════════╪═══╪══════════════╪═══════════════╪═════════════╪══════════════╡
│ 1        ┆ 2025-01-01    ┆ 2025-01-01    ┆ 1             ┆ … ┆ 18.0         ┆ 2.5           ┆ 0.0         ┆ 0.0          │
│          ┆ 00:18:38      ┆ 00:26:59      ┆               ┆   ┆              ┆               ┆             ┆              │
│ 1        ┆ 2025-01-01    ┆ 2025-01-01    ┆ 1             ┆ … ┆ 12.12        ┆ 2.5           ┆ 0.0         ┆ 0.0          │
│          ┆ 00:32:40      ┆ 00:35:13      ┆               ┆   ┆              ┆               ┆             ┆              │
│ 1        ┆ 2025-01-01    ┆ 2025-01-01    ┆ 1             ┆ … ┆ 12.1         ┆ 2.5           ┆ 0.0         ┆ 0.0          │
│          ┆ 00:44:04      ┆ 00:46:01      ┆               ┆   ┆              ┆               ┆             ┆              │
│ 2        ┆ 2025-01-01    ┆ 2025-01-01    ┆ 3             ┆ … ┆ 9.7          ┆ 0.0           ┆ 0.0         ┆ 0.0          │
│          ┆ 00:14:27      ┆ 00:20:01      ┆               ┆   ┆              ┆               ┆             ┆              │
│ 2        ┆ 2025-01-01    ┆ 2025-01-01    ┆ 3             ┆ … ┆ 8.3          ┆ 0.0           ┆ 0.0         ┆ 0.0          │
│          ┆ 00:21:34      ┆ 00:25:06      ┆               ┆   ┆              ┆               ┆             ┆              │
└──────────┴───────────────┴───────────────┴───────────────┴───┴──────────────┴───────────────┴─────────────┴──────────────┘
Starting Pipeline Phase 2: Medallion Architecture...
.venv/bin/python src/03_medallion_pipeline.py
Initiating Medallion Architecture Forge...
Crafting Silver Layer (Clean Data)...
Silver dataset saved to: data/silver/clean_taxi_data.parquet
Forging Gold Layer (Business Aggregations)...
Gold dataset saved to: data/gold/daily_revenue_metrics.parquet

Pipeline execution complete. All layers forged.
Starting Pipeline Phase 3: DuckDB Analytics...
.venv/bin/python src/04_analyze_gold.py
Summoning DuckDB to analyze Gold metrics...

┌─────────────┬─────────────────────┬─────────────┬──────────────────────┐
│ pickup_date │ total_daily_revenue │ total_trips │ avg_revenue_per_trip │
│    date     │       double        │   uint32    │        double        │
├─────────────┼─────────────────────┼─────────────┼──────────────────────┤
│ 2025-12-04  │   4037619.949999844 │      127280 │                31.72 │
│ 2025-12-11  │  3992923.7899998957 │      127095 │                31.42 │
│ 2025-10-16  │  3898324.6999999117 │      122966 │                 31.7 │
│ 2025-12-12  │  3872343.3999999007 │      123976 │                31.23 │
│ 2025-10-23  │    3846401.97999993 │      122825 │                31.32 │
└─────────────┴─────────────────────┴─────────────┴──────────────────────┘

Starting Pipeline Phase 4: Network Database Load...
.venv/bin/python src/05_load_to_postgres.py
Scanning Gold dataset into memory...
Initiating network transfer: Pushing 369 rows to the i3 Command Center...
Transfer complete! The data has successfully crossed the network.
End-to-End Pipeline Complete!



docker compose up -d


docker ps

awslocal s3 mb s3://taxi-data-lake

awslocal s3 ls s3://taxi-data-lake --recursive
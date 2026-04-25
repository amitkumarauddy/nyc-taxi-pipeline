# NYC Taxi Data Pipeline

A modern data engineering pipeline that processes NYC yellow taxi trip data through a medallion architecture (Bronze → Silver → Gold layers) using Python, Polars, DuckDB, and cloud services.

## Features

- **Data Processing**: Process 48M+ taxi records with Polars lazy evaluation
- **Medallion Architecture**: Bronze (raw + metadata), Silver (cleaned), Gold (aggregated metrics)
- **Analytics**: DuckDB-powered business intelligence
- **Cloud Integration**: PostgreSQL and S3 (LocalStack) support
- **Containerization**: Docker support for reproducible deployments
- **Orchestration Ready**: Airflow DAGs for production scheduling

## Prerequisites

- **Python 3.12+**
- **Docker & Docker Compose** (for containerized runs)
- **Make** (for local development)
- **4GB+ disk space** for taxi data

## Quick Start

### Option 1: Local Development (Recommended for Development)

```bash
# 1. Setup Python environment
sudo apt install python3.12-venv make
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download data (optional - ~4GB)
chmod +x src/00_download_year.sh
./src/00_download_year.sh

# 4. Run full pipeline
make run-all
```

### Option 2: Docker (Recommended for Production/Reproducibility)

```bash
# 1. Download data locally first
chmod +x src/00_download_year.sh
./src/00_download_year.sh

# 2. Run pipeline in Docker
docker compose -f docker-compose.pipeline.yml run --rm pipeline
```

### Option 3: With Cloud Services

```bash
# Start LocalStack for S3 mock
docker compose up -d

# Run pipeline (includes S3 upload)
docker compose -f docker-compose.pipeline.yml run --rm pipeline
```

## Detailed Setup

### Local Setup

1. **Install System Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.12-venv make wget
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Add this to ~/.bashrc for persistence
   ```

3. **Install Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NYC Taxi Data** (~4GB)
   ```bash
   chmod +x src/00_download_year.sh
   ./src/00_download_year.sh
   ```

### Docker Setup

1. **Build Pipeline Image**
   ```bash
   docker compose -f docker-compose.pipeline.yml build
   ```

2. **Run with Data Volume**
   ```bash
   docker compose -f docker-compose.pipeline.yml run --rm pipeline
   ```

## Usage

### Makefile Commands (Local Development)

```bash
make help          # Show available commands
make install       # Install Python dependencies
make run-all       # Execute complete pipeline
make clean         # Remove generated Parquet files
```

### Docker Commands

```bash
# Run full pipeline
docker compose -f docker-compose.pipeline.yml run --rm pipeline

# Run with LocalStack S3
docker compose up -d  # Start LocalStack
docker compose -f docker-compose.pipeline.yml run --rm pipeline

# Build custom image
docker build -t nyc-taxi-pipeline .

# Run Airflow (orchestration)
cd airflow-ops
docker compose up -d
```

### Pipeline Phases

The pipeline runs 5 sequential phases:

1. **Ingestion & Cleaning**: Load and filter raw taxi data
2. **Medallion Architecture**: Create Bronze/Silver/Gold layers
3. **DuckDB Analytics**: Business intelligence queries
4. **PostgreSQL Load**: Export to relational database
5. **S3 Upload**: Cloud storage backup

## Architecture

```
Raw Data (Parquet)
    ↓
Bronze Layer (Raw + Metadata)
    ↓
Silver Layer (Cleaned Data)
    ↓
Gold Layer (Aggregated Metrics)
    ↓
Analytics + PostgreSQL + S3
```

### Technologies

- **Polars**: High-performance DataFrame processing
- **DuckDB**: Embedded analytical database
- **PostgreSQL**: Relational data warehouse
- **LocalStack**: AWS services mock
- **Docker**: Containerization
- **Airflow**: Workflow orchestration

## Sample Output

```
Starting Pipeline Phase 1: Ingestion & Cleaning...
Initiating lazy scan of multiple months...
Total rows before cleaning: 48,722,602
Executing data quality filters...
Total rows after cleaning: 35,604,835
Bad records eliminated: 13,117,767

Starting Pipeline Phase 2: Medallion Architecture...
Crafting Bronze Layer (Adding Ingestion Timestamps)...
Bronze dataset saved to: data/bronze/raw_taxi_data_with_metadata.parquet
Crafting Silver Layer (Clean Data)...
Silver dataset saved to: data/silver/clean_taxi_data.parquet
Forging Gold Layer (Business Aggregations)...
Gold dataset saved to: data/gold/daily_revenue_metrics.parquet

Starting Pipeline Phase 3: DuckDB Analytics...
Summoning DuckDB to analyze Gold metrics...

┌─────────────┬─────────────────────┬─────────────┬──────────────────────┐
│ pickup_date │ total_daily_revenue │ total_trips │ avg_revenue_per_trip │
│    date     │       double        │   uint32    │        double        │
├─────────────┼─────────────────────┼─────────────┼──────────────────────┤
│ 2025-12-04  │   4037619.949999844 │      127280 │                31.72 │
│ 2025-12-11  │  3992923.7899998957 │      127095 │                31.42 │
│ 2025-10-16  │  3898324.6999999117 │      122966 │                 31.7 │
└─────────────┴─────────────────────┴─────────────┴──────────────────────┘

Starting Pipeline Phase 4: Network Database Load...
Scanning Gold dataset into memory...
Initiating network transfer: Pushing 369 rows to the i3 Command Center...
Transfer complete! The data has successfully crossed the network.

Starting Pipeline Phase 5: Cloud S3 Upload...
Connecting to local AWS S3...
Uploading Medallion metrics to s3://taxi-data-lake/gold/daily_revenue_metrics.parquet...
Upload complete! The Gold dataset is securely stored in the Data Lake.

End-to-End Pipeline Complete!
```

## Configuration

### Environment Variables

- `PYTHON`: Python executable path (auto-detected in Docker)
- `target_ip`: PostgreSQL server IP (default: 192.168.29.224)

### Data Locations

- Raw data: `data/raw/`
- Bronze layer: `data/bronze/`
- Silver layer: `data/silver/`
- Gold layer: `data/gold/`

## Troubleshooting

### Common Issues

1. **"No such file or directory" for Python**
   - Ensure virtual environment is activated: `source .venv/bin/activate`

2. **S3 upload fails**
   - Start LocalStack: `docker compose up -d`
   - Create bucket: `awslocal s3 mb s3://taxi-data-lake`

3. **PostgreSQL connection fails**
   - Update `target_ip` in `src/05_load_to_postgres.py`
   - Ensure PostgreSQL is running and accessible

4. **Docker build fails**
   - Ensure Docker daemon is running
   - Check available disk space (>4GB)

### Performance Notes

- Pipeline processes ~49M records in ~5-10 minutes
- Memory usage: ~8GB peak during processing
- Disk usage: ~12GB for all layers + raw data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper testing
4. Submit a pull request

## License

This project is open source. See LICENSE file for details.
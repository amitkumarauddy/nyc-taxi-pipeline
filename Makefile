# Variables
PYTHON = /home/auddy/nyc-taxi-pipeline/.venv/bin/python

# The "help" command shows what this Makefile can do
help:
	@echo "Available commands:"
	@echo "  make install    - Install Python dependencies"
	@echo "  make run-all    - Execute the entire end-to-end pipeline"
	@echo "  make clean      - Delete generated parquet files to start fresh"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

clean:
	rm -f data/bronze/*.parquet
	rm -f data/silver/*.parquet
	rm -f data/gold/*.parquet
	@echo "Bronze, Silver, and Gold folders cleared."

run-all:
	@echo "Starting Pipeline Phase 1: Ingestion & Cleaning..."
	$(PYTHON) src/02_clean_and_combine.py
	@echo "Starting Pipeline Phase 2: Medallion Architecture..."
	$(PYTHON) src/03_medallion_pipeline.py
	@echo "Starting Pipeline Phase 3: DuckDB Analytics..."
	$(PYTHON) src/04_analyze_gold.py
	@echo "Starting Pipeline Phase 4: Network Database Load..."
	$(PYTHON) src/05_load_to_postgres.py
	@echo "Starting Pipeline Phase 5: Cloud S3 Upload..."
	$(PYTHON) src/06_upload_to_s3.py
	@echo "End-to-End Pipeline Complete!"
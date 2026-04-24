import polars as pl
from datetime import datetime

raw_data_path = "data/raw/yellow_tripdata_2025-*.parquet"
bronze_data_path = "data/bronze/raw_taxi_data_with_metadata.parquet"
silver_data_path = "data/silver/clean_taxi_data.parquet"
gold_data_path = "data/gold/daily_revenue_metrics.parquet"

print("Initiating Medallion Architecture Forge...")

# ==========================================
# 1. RAW -> BRONZE (Injecting Metadata)
# ==========================================
print("Crafting Bronze Layer (Adding Ingestion Timestamps)...")

# Capture the exact moment the pipeline runs
current_time = datetime.now()

bronze_lazy_df = (
    pl.scan_parquet(raw_data_path)
    # Add a new column with the current timestamp
    .with_columns(pl.lit(current_time).alias("ingestion_timestamp"))
)

bronze_lazy_df.sink_parquet(bronze_data_path)
print(f"Bronze dataset saved to: {bronze_data_path}")

# ==========================================
# 2. BRONZE -> SILVER (The Purge)
# ==========================================
print("Crafting Silver Layer (Clean Data)...")
silver_lazy_df = (
    pl.scan_parquet(bronze_data_path) # Now reading from Bronze!
    .filter(
        (pl.col("trip_distance") > 0) & 
        (pl.col("fare_amount") > 0) &
        (pl.col("passenger_count") > 0)
    )
)

silver_lazy_df.sink_parquet(silver_data_path)
print(f"Silver dataset saved to: {silver_data_path}")

# ==========================================
# 3. SILVER -> GOLD (The Boss Metrics)
# ==========================================
print("Forging Gold Layer (Business Aggregations)...")
gold_lazy_df = (
    pl.scan_parquet(silver_data_path)
    .with_columns(pl.col("tpep_pickup_datetime").dt.date().alias("pickup_date"))
    .group_by("pickup_date")
    .agg([
        pl.sum("total_amount").alias("total_daily_revenue"),
        pl.mean("trip_distance").alias("avg_trip_distance"),
        pl.len().alias("total_trips")
    ])
    .sort("pickup_date")
)

gold_lazy_df.sink_parquet(gold_data_path)
print(f"Gold dataset saved to: {gold_data_path}")
print("\nPipeline execution complete. All layers forged.")
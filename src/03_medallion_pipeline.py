import polars as pl

bronze_data_path = "data/yellow_tripdata_2025-*.parquet"
silver_data_path = "data/silver/clean_taxi_data.parquet"
gold_data_path = "data/gold/daily_revenue_metrics.parquet"

print("Initiating Medallion Architecture Forge...")

# ==========================================
# 1. BRONZE -> SILVER (The Purge)
# ==========================================
print("Crafting Silver Layer (Clean Data)...")
silver_lazy_df = (
    pl.scan_parquet(bronze_data_path)
    .filter(
        (pl.col("trip_distance") > 0) & 
        (pl.col("fare_amount") > 0) &
        (pl.col("passenger_count") > 0)
    )
)

# Stream the clean data directly to a new Parquet file
silver_lazy_df.sink_parquet(silver_data_path)
print(f"Silver dataset saved to: {silver_data_path}")

# ==========================================
# 2. SILVER -> GOLD (The Boss Metrics)
# ==========================================
print("Forging Gold Layer (Business Aggregations)...")

# We scan the newly created Silver file, extract the date, and group the stats.
gold_lazy_df = (
    pl.scan_parquet(silver_data_path)
    # Extract just the date (YYYY-MM-DD) from the datetime column
    .with_columns(pl.col("tpep_pickup_datetime").dt.date().alias("pickup_date"))
    # Group by that day
    .group_by("pickup_date")
    # Calculate the boss-level metrics
    .agg([
        pl.sum("total_amount").alias("total_daily_revenue"),
        pl.mean("trip_distance").alias("avg_trip_distance"),
        pl.len().alias("total_trips")
    ])
    # Sort chronologically
    .sort("pickup_date")
)

# Stream the final business metrics to disk
gold_lazy_df.sink_parquet(gold_data_path)
print(f"Gold dataset saved to: {gold_data_path}")
print("\nPipeline execution complete. All layers forged.")
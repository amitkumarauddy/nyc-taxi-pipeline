import polars as pl

# 1. Define the path to your data
data_path = "data/raw/yellow_tripdata_2025-01.parquet"

# 2. Use Polars to lazily scan the file (super fast, uses very little memory)
print("Scanning dataset with Polars...")
df = pl.scan_parquet(data_path)

# 3. Let's do a basic transformation: Filter out zero-passenger rides and calculate total cost
clean_df = (
    df.filter(pl.col("passenger_count") > 0)
    .with_columns(
        (pl.col("fare_amount") + pl.col("tip_amount")).alias("total_customer_cost")
    )
)

# 4. Execute the query and show the first 5 rows
print(clean_df.head(5).collect())

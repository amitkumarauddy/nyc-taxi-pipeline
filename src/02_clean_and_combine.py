import polars as pl

# 1. THE WILDCARD (Globbing)
# By using the asterisk (*), we tell Polars to grab any file that matches this pattern.
# This single line automatically targets both your January and February files.
data_path = "../data/yellow_tripdata_2025-*.parquet"

print("Initiating lazy scan of multiple months...")

# 2. CREATE THE LAZY GRAPH
# scan_parquet registers the files but doesn't load them into memory yet.
lazy_df = pl.scan_parquet(data_path)

# Let's do a quick calculation to see our starting HP (row count)
initial_count = lazy_df.select(pl.len()).collect().item()
print(f"Total rows before cleaning: {initial_count:,}")

# 3. APPLY DATA QUALITY SHIELDS
# We chain our filters together using the '&' (AND) operator.
print("Executing data quality filters...")
clean_lazy_df = lazy_df.filter(
    (pl.col("trip_distance") > 0) & 
    (pl.col("fare_amount") > 0) &
    (pl.col("passenger_count") > 0)
)

# 4. TRIGGER THE EXECUTION
# The .collect() command tells Polars to actually perform the work.
final_df = clean_lazy_df.collect()

# 5. BATTLE REPORT
final_count = final_df.height
rows_removed = initial_count - final_count

print(f"Total rows after cleaning: {final_count:,}")
print(f"Bad records eliminated: {rows_removed:,}")

print("\n--- Clean Dataset Preview ---")
print(final_df.head(5))

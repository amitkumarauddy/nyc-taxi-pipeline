import polars as pl

# 1. The Connection String (The network bridge between your i7 and i3)
# Format: postgresql://username:password@host_ip:port/database_name
target_ip = "192.168.29.224" 
db_uri = f"postgresql://postgres:admin123@{target_ip}:5432/postgres"

# 2. Load the Gold data from the i7's local hard drive
gold_data_path = "data/gold/daily_revenue_metrics.parquet"
print("Scanning Gold dataset into memory...")
df = pl.read_parquet(gold_data_path)

# 3. Execute the Teleportation
print(f"Initiating network transfer: Pushing {df.height} rows to the i3 Command Center...")

# Polars automatically creates the table and infers the SQL data types!
df.write_database(
    table_name="gold_daily_revenue", 
    connection=db_uri, 
    if_table_exists="replace"
)

print("Transfer complete! The data has successfully crossed the network.")
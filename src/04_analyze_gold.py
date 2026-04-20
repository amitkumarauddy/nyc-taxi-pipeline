import duckdb

# Point directly to your freshly forged Gold dataset
gold_data_path = "../data/gold/daily_revenue_metrics.parquet"

print("Summoning DuckDB to analyze Gold metrics...\n")

# Write standard SQL to find the top 5 most profitable days, 
# calculating a new metric (revenue per trip) on the fly.
query = f"""
    SELECT 
        pickup_date,
        total_daily_revenue,
        total_trips,
        ROUND(total_daily_revenue / total_trips, 2) AS avg_revenue_per_trip
    FROM '{gold_data_path}'
    WHERE total_trips > 1000
    ORDER BY total_daily_revenue DESC
    LIMIT 5;
"""

# Execute the query and display the results in the terminal
duckdb.sql(query).show()

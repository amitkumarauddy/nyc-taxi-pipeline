#!/bin/bash

echo "Initiating mass data extraction..."
echo "Target: NYC Yellow Taxi Records (Full Year 2025)"

# Loop through months 01 to 12
for i in {01..12}; do
  url="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-${i}.parquet"
  echo "Downloading Month: $i..."
  
  # wget -nc prevents downloading if the file already exists
  # -qO- suppresses the giant progress bar so the terminal stays clean
  # -P routes the downloaded file straight into your data folder
  wget -nc -P data/ "$url"
done

echo "Extraction complete. The vault is full."
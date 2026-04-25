# 1. BASE IMAGE: Start with a lightweight, official Python Linux environment
FROM python:3.12-slim

# 2. Install system dependencies needed for the pipeline
RUN apt-get update && apt-get install -y \
    wget \
    make \
    && rm -rf /var/lib/apt/lists/*

# 3. WORKSPACE: Create a folder inside the container called /app and move into it
WORKDIR /app

# 4. DEPENDENCIES: Copy your requirements list into the container
COPY requirements.txt .

# 5. INSTALL: Run the pip install inside the container
# (--no-cache-dir keeps the image size small by deleting the installer files after)
RUN pip install --no-cache-dir -r requirements.txt

# 6. SOURCE CODE: Copy your Python scripts and Makefile into the container
COPY src/ /app/src/
COPY Makefile /app/

# 7. DATA DIRECTORY: Create data directory structure (data will be mounted as volume)
RUN mkdir -p /app/data/raw /app/data/bronze /app/data/silver /app/data/gold

# 8. Make scripts executable
RUN chmod +x /app/src/00_download_year.sh

# 9. DEFAULT COMMAND: Run the full pipeline instead of just cleaning
# Note: Data should be mounted as volume or downloaded first
CMD ["make", "run-all"]

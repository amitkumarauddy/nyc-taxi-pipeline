# 1. BASE IMAGE: Start with a lightweight, official Python Linux environment
FROM python:3.12-slim

# 2. WORKSPACE: Create a folder inside the container called /app and move into it
WORKDIR /app

# 3. DEPENDENCIES: Copy your requirements list into the container
COPY requirements.txt .

# 4. INSTALL: Run the pip install inside the container
# (--no-cache-dir keeps the image size small by deleting the installer files after)
RUN pip install --no-cache-dir -r requirements.txt

# 5. SOURCE CODE: Copy your Python scripts into the container's /app/src folder
COPY src/ /app/src/

# 6. DEFAULT COMMAND: What should the container do when it wakes up?
# Let's have it run your Polars cleaning script.
CMD ["python", "src/02_clean_and_combine.py"]

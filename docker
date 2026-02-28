# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but often useful)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if you have one, otherwise install pandas directly
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pandas

# Copy ETL script (and optionally sample CSVs if present)
COPY etl.py .

# Default input/output file names (the script uses these)
# If you have sample CSVs, you can COPY them too:
# COPY input_data.csv .
# (By default, etl.py will look for "input_data.csv" in /app)

# Run the ETL process
CMD ["python", "etl.py"]

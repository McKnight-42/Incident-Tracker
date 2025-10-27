# Base image
FROM python:3.11-slim

# Dockerfile
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY app/ ./app

# Copy entrypoint script from repo root
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

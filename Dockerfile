# Base Image
FROM python:3.11-slim

# Install the dependencies required for Playwright
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright 
RUN playwright install --with-deps chromium

# Run the script
CMD ["python", "./automation/script.py"]


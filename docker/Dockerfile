# Use a recent Python version - slim variant keeps image smaller
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for psycopg2 & others)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy & install Python dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code (but we'll override with volume in compose)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run with uvicorn + reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
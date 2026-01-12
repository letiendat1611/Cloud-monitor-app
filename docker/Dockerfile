# Use a recent Python version - slim variant keeps image smaller
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Combine apt updates and cleanups to reduce layers and image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    gnupg \
    lsb-release \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy & install Python dependencies first (great for caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copy your code (will be overridden by volume in dev)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run with uvicorn + reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
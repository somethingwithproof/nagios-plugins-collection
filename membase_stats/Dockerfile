# Use the official Python image from the Docker Hub
FROM python:3.14.0a3-slim

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set a non-root user for security purposes
RUN useradd -m appuser

# Install system dependencies and clean up cache to reduce image size
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch to the non-root user
USER appuser

# Set the working directory
WORKDIR /membase_stats

# Copy and install dependencies with safety checks
COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY --chown=appuser:appuser . .

# Set default command (adjust as needed based on your application)
CMD ["python", "app.py"]

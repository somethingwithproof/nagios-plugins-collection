# Use the official Python image from the Docker Hub
FROM python:3.9

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Create a directory to hold the application
WORKDIR /membase_stats

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application
COPY . .

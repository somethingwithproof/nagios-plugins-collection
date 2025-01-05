# Use the official Python image from the Docker Hub
FROM python:3.14.0a3-slim

# Set a non-root user for security purposes
RUN useradd -m appuser

# Set the working directory
WORKDIR /app

# Copy and install dependencies with safety checks
COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY --chown=appuser:appuser . .

# Switch to the non-root user
USER appuser

# Set default command (adjust as needed based on your application)
CMD ["python", "check_status.py"]

# Nagios Plugins Collection Docker Image
# Multi-stage build for minimal image size

# Build stage
FROM python:3.12-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt requirements-lock.txt ./
COPY pyproject.toml setup.py ./
COPY src/ ./src/

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir .

# Runtime stage
FROM python:3.12-slim

LABEL maintainer="Thomas Vincent <thomas@thomasvincent.io>"
LABEL description="Nagios Plugins Collection - Production monitoring plugins"
LABEL version="2.0.0"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    dnsutils \
    openssh-client \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set up environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash nagios
USER nagios
WORKDIR /home/nagios

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import nagios_plugins; print('OK')" || exit 1

# Default command shows help
CMD ["python", "-m", "nagios_plugins", "--help"]

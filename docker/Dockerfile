# syntax=docker/dockerfile:1.7

# Builder: install deps and build wheel
FROM python:3.12-slim AS builder
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
COPY tests /app/tests
RUN python -m pip install --upgrade pip build && \
    python -m build

# Runtime: minimal image with package installed
FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Install runtime deps only from the built wheel
COPY --from=builder /app/dist /tmp/dist
RUN python -m pip install --upgrade pip && \
    pip install /tmp/dist/*-py3-none-any.whl && \
    rm -rf /tmp/dist
# Default entrypoint runs a smoke check; override with commands
ENTRYPOINT ["nagios-plugins-collection"]
CMD ["--help"]

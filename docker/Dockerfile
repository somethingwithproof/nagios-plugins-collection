# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
# syntax=docker/dockerfile:1.7

# Builder: collect wheels for the package and its runtime plugin extras.
FROM python:3.14-slim AS builder
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY pyproject.toml README.md LICENSE /app/
COPY packaging /app/packaging
COPY src /app/src
RUN python -m pip install --only-binary=:all: --require-hashes -r packaging/build-requirements.txt && \
    python -m build --no-isolation --wheel && \
    python -m pip download --only-binary=:all: --require-hashes \
        --dest /wheels -r packaging/container-requirements.txt && \
    cp /app/dist/*.whl /wheels/

# Test controller: runtime extras plus the development test tools.
FROM builder AS tests
COPY tests /app/tests
COPY scripts /app/scripts
RUN python -m pip install --only-binary=:all: --require-hashes -r packaging/test-requirements.txt && \
    python -m pip install --only-binary=:all: --no-deps /app/dist/*.whl
CMD ["pytest", "-q"]

# Runtime: minimal image with package installed
FROM python:3.14-slim AS runtime
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
# Install runtime deps only from the built wheel
COPY --from=builder /wheels /tmp/wheels
COPY packaging/container-requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-index --find-links=/tmp/wheels --only-binary=:all: \
        --require-hashes -r /tmp/requirements.txt && \
    python -m pip install --only-binary=:all: --no-index --no-deps /tmp/wheels/nagios_plugins_collection-*.whl && \
    rm -rf /tmp/wheels && \
    groupadd --system --gid 10001 nagios && \
    useradd --system --uid 10001 --gid nagios --home-dir /app --shell /usr/sbin/nologin nagios
USER nagios
# Default command displays help; callers can select any installed plugin.
CMD ["check_website_status", "--help"]

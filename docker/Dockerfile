# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
# syntax=docker/dockerfile:1.7

# uv exports hash-pinned requirements from uv.lock; pip installs them wheel-only.
FROM ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 AS uv

# Builder: collect wheels for the package and its runtime plugin extras.
FROM python:3.14-slim AS builder
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY --from=uv /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock README.md LICENSE /app/
COPY src /app/src
RUN uv export --locked --no-emit-project --only-group build -o /tmp/build-requirements.txt && \
    python -m pip install --only-binary=:all: --require-hashes -r /tmp/build-requirements.txt && \
    python -m build --no-isolation --wheel && \
    mkdir /wheels && \
    uv export --locked --no-dev --no-emit-project --extra all -o /wheels/requirements.txt && \
    python -m pip download --only-binary=:all: --require-hashes \
        --dest /wheels -r /wheels/requirements.txt && \
    cp /app/dist/*.whl /wheels/

# Test controller: runtime extras plus the development test tools.
FROM builder AS tests
COPY tests /app/tests
COPY scripts /app/scripts
COPY packaging /app/packaging
RUN uv export --locked --no-emit-project --all-extras --no-default-groups --group test -o /tmp/test-requirements.txt && \
    python -m pip install --only-binary=:all: --require-hashes -r /tmp/test-requirements.txt && \
    python -m pip install --only-binary=:all: --no-deps /app/dist/*.whl
CMD ["pytest", "-q"]

# Runtime: minimal image with package installed
FROM python:3.14-slim AS runtime
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
# Apply Debian security updates the base image has not picked up yet.
RUN apt-get update && \
    apt-get -y upgrade && \
    rm -rf /var/lib/apt/lists/*
# Install runtime deps only from the built wheel, then remove pip: nothing at
# runtime needs it, and its vendored packages are otherwise scanned as part of
# the image.
COPY --from=builder /wheels /tmp/wheels
RUN python -m pip install --no-index --find-links=/tmp/wheels --only-binary=:all: \
        --require-hashes -r /tmp/wheels/requirements.txt && \
    python -m pip install --only-binary=:all: --no-index --no-deps /tmp/wheels/nagios_plugins_collection-*.whl && \
    python -m pip uninstall --yes pip && \
    rm -rf /tmp/wheels && \
    groupadd --system --gid 10001 nagios && \
    useradd --system --uid 10001 --gid nagios --home-dir /app --shell /usr/sbin/nologin nagios
USER 10001:10001
# Default command displays help; callers can select any installed plugin.
CMD ["check_website_status", "--help"]

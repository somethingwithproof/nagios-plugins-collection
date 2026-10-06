# syntax=docker/dockerfile:1.7

# Builder: collect wheels for the package and its runtime plugin extras.
FROM python:3.14-slim AS builder
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN python -m pip install --upgrade pip build && \
    python -m build --wheel && \
    for package in /app/dist/*.whl; do \
        python -m pip wheel --only-binary=:all: --wheel-dir /wheels \
            "$package[mongodb,ssh,cli,schema,dns,k8s,pg,redis,aws]"; \
    done

# Runtime: minimal image with package installed
FROM python:3.14-slim AS runtime
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Install runtime deps only from the built wheel
COPY --from=builder /wheels /tmp/wheels
RUN python -m pip install --no-index --find-links=/tmp/wheels \
        'nagios-plugins-collection[mongodb,ssh,cli,schema,dns,k8s,pg,redis,aws]' && \
    rm -rf /tmp/wheels && \
    groupadd --system --gid 10001 nagios && \
    useradd --system --uid 10001 --gid nagios --home-dir /app --shell /usr/sbin/nologin nagios
USER nagios
# Default entrypoint runs a smoke check; override with commands
ENTRYPOINT ["check_website_status"]
CMD ["--help"]

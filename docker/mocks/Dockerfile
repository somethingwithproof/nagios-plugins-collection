# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
# Simple FastAPI mock server for E2E tests (OAuth2 token + Prometheus API)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir --only-binary=:all: --require-hashes -r /tmp/requirements.txt && \
    groupadd --system --gid 10001 nagios && \
    useradd --system --uid 10001 --gid nagios --home-dir /app --shell /usr/sbin/nologin nagios

WORKDIR /app
COPY app.py /app/app.py

EXPOSE 8000

USER nagios
HEALTHCHECK --interval=5s --timeout=3s --retries=15 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).close()"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

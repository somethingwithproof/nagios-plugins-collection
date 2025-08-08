FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt ./

# Install build dependencies for psycopg2
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    && apk add --no-cache postgresql-libs \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY . .

CMD ["python", "vertigo_status_checker.py"]

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ספריות בניה מינימליות ל-confluent-kafka ול-psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    librdkafka-dev gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# שים לב לנתיבי COPY בהתאם ל-build context מה-compose (../..)
COPY services/ingest/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY services/ingest /app/services/ingest

CMD ["python", "-u", "services/ingest/consumer.py"]

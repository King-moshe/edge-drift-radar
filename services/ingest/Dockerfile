# Consumer Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \ 
    librdkafka-dev gcc &&     rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY services/ingest/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY services/ingest /app/services/ingest

CMD ["python", "-u", "services/ingest/consumer.py"]

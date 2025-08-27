# Agent Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

# Install minimal build deps for confluent-kafka wheels fallback
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    librdkafka-dev gcc &&     rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY agent/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY agent /app/agent
EXPOSE 8080

CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8080"]

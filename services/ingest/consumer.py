import os, json, time, signal, sys
from typing import Dict, Any
from confluent_kafka import Consumer, KafkaException, KafkaError
import psycopg2

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "redpanda:9092")
TOPIC = os.getenv("TOPIC", "edr.telemetry")
GROUP_ID = os.getenv("GROUP_ID", "edr-consumer")
PGHOST = os.getenv("PGHOST", "timescaledb")
PGPORT = int(os.getenv("PGPORT", "5432"))
PGUSER = os.getenv("PGUSER", "edr")
PGPASSWORD = os.getenv("PGPASSWORD", "edrpass")
PGDATABASE = os.getenv("PGDATABASE", "edr")

conf = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
}

def connect_db():
    conn = psycopg2.connect(
        host=PGHOST, port=PGPORT, user=PGUSER, password=PGPASSWORD, dbname=PGDATABASE
    )
    conn.autocommit = True
    return conn

def upsert_metric(cur, ts: float, site_id: str, device_id: str, stream_id: str, metric: str, value: float, labels: Dict[str, Any]):
    cur.execute(
        """
        INSERT INTO metrics_raw (ts, site_id, device_id, stream_id, metric, value, labels)
        VALUES (to_timestamp(%s), %s, %s, %s, %s, %s, %s::jsonb)
        """,
        (ts, site_id, device_id, stream_id, metric, value, json.dumps(labels)),
    )

def handle_message(cur, key_bytes, value_bytes):
    data = json.loads(value_bytes.decode("utf-8"))
    ts = float(data.get("ts", time.time()))
    site_id = data["site_id"]
    device_id = data["device_id"]
    stream_id = data["stream_id"]
    payload = data.get("payload", {})
    labels = data.get("labels", {})

    # Derive metrics
    now = time.time()
    freshness_sec = max(0.0, now - ts)
    latency_ms = float(payload.get("latency_ms", -1.0))

    # Write freshness
    upsert_metric(cur, ts, site_id, device_id, stream_id, "freshness_sec", freshness_sec, labels)

    # Write latency if provided
    if latency_ms >= 0:
        upsert_metric(cur, ts, site_id, device_id, stream_id, "latency_ms", latency_ms, labels)

def main():
    c = Consumer(conf)
    c.subscribe([TOPIC])
    print(f"👂 Listening on topic={TOPIC} brokers={BOOTSTRAP_SERVERS} group={GROUP_ID}")
    conn = connect_db()
    cur = conn.cursor()

    running = True
    def shutdown(signum, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while running:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                raise KafkaException(msg.error())
            try:
                handle_message(cur, msg.key(), msg.value())
                print(f"✅ persisted metrics for key={msg.key()} offset={msg.offset()}")
            except Exception as e:
                print(f"❌ failed to persist: {e}", file=sys.stderr)
    finally:
        c.close()
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()

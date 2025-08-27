from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from confluent_kafka import Producer
import json
import os
import time

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "redpanda:9092")
TOPIC = os.getenv("TOPIC", "edr.telemetry")

conf = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "client.id": "edr-agent",
    "enable.idempotence": True,
}

p = Producer(conf)

app = FastAPI(title="EDR Agent", version="0.1.0")


class Telemetry(BaseModel):
    ts: Optional[float] = Field(default_factory=lambda: time.time())
    site_id: str
    device_id: str
    stream_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    labels: Dict[str, Any] = Field(default_factory=dict)


def _delivery(err, msg):
    if err is not None:
        # In MVP we just log; later: route to retry/Dead Letter
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"""✅ Delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}""")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/telemetry")
async def telemetry(t: Telemetry):
    try:
        key = t.device_id.encode("utf-8")
        value = json.dumps(t.dict()).encode("utf-8")
        p.produce(TOPIC, key=key, value=value, callback=_delivery)
        p.poll(0)
        return {"status": "queued", "topic": TOPIC}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
def shutdown():
    p.flush(10)

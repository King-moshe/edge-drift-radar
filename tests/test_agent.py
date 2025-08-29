from fastapi.testclient import TestClient
from agent.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_telemetry_basic():
    payload = {
        "site_id": "s1",
        "device_id": "d1",
        "stream_id": "cam1",
        "payload": {"latency_ms": 123}
    }
    r = client.post("/telemetry", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] in ("queued", "ok")

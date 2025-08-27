-- Day 2 schema draft for metrics
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS metrics_raw (
  ts TIMESTAMPTZ NOT NULL,
  site_id TEXT NOT NULL,
  device_id TEXT NOT NULL,
  stream_id TEXT NOT NULL,
  metric TEXT NOT NULL,
  value DOUBLE PRECISION,
  labels JSONB DEFAULT '{}'::jsonb
);

SELECT create_hypertable('metrics_raw', 'ts', if_not_exists => TRUE);

CREATE MATERIALIZED VIEW IF NOT EXISTS metrics_pivot AS
SELECT
  ts,
  site_id, device_id, stream_id,
  MAX(value) FILTER (WHERE metric = 'completeness')    AS completeness,
  MAX(value) FILTER (WHERE metric = 'latency_ms_p95')  AS latency_ms_p95,
  MAX(value) FILTER (WHERE metric = 'freshness_sec')   AS freshness_sec
FROM metrics_raw
GROUP BY ts, site_id, device_id, stream_id
WITH NO DATA;

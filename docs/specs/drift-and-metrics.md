# Data Quality & Drift — Initial Specification (Day 2)

## Drift Types (v0)
- **Schema Drift**: field additions/removals/renames, type changes, unit changes.
- **Data Drift**: statistical shift in distributions (PSI, KS).
- **Concept Drift**: change in relationship between features→target over time (ADWIN/HDDM family).

## Core Quality Metrics (per sensor/stream)
- **completeness** (0..1)
- **latency_ms** (p95/p99)
- **freshness_sec**
- **timeliness** (OK/WARN/CRIT)
- **validity** (schema/type/range via Great Expectations)
- **accuracy_proxy** (domain checks)
- **availability** (heartbeat up/down)
- **throughput_msgs_s**

## Drift Indicators (stream-level)
- **psi_{field}**
- **ks_{field}**
- **hddm_{model}**

## Alerting (v0)
- `latency_ms.p95 > 200` → WARN, `> 500` → CRIT
- `freshness_sec > 60` → WARN, `> 300` → CRIT
- `psi_* > 0.25` → WARN, `> 0.5` → CRIT

## Naming/Tags
`site_id`, `device_id`, `stream_id`, `sensor_type`, `firmware_version`, `schema_version`.

## Storage
- Metrics → TimescaleDB (`metrics_raw` hypertable).
- Raw payloads (optional) → S3-compatible object storage.

## Next
- Prometheus exporters on Edge; unify units; calibrate thresholds with pilot data.

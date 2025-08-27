# Edge Drift Radar

Real-time data quality & concept drift monitoring at the edge.

## Goals (Sprint 1 / Week 1)
- Repo + CI bootstrap
- Local dev stack (Docker Compose skeleton)
- Agent skeleton to be added in Day 3
- Observability stack wiring to be added in Day 4–5

## Tech (initial)
- Python (FastAPI) for agent/services
- Redpanda (Kafka API), TimescaleDB, Grafana
- Docker + Docker Compose
- GitHub Actions (CI)

## Getting Started (Day 1)
1. Ensure Docker Desktop is installed and running.
2. Clone this repo and open in VS Code.
3. Run: `docker compose version` to verify Compose v2.

## Repo Conventions
- **Branching:** `main`, feature branches: `feat/<scope>`, `chore/*`, `fix/*`.
- **Commits:** Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`).
- **Issues:** Managed in Jira; link PRs to issues (e.g., EDR-1).

## Structure (will evolve)
```
.
├─ docs/
│  └─ adrs/
├─ infra/
│  └─ docker-compose/
├─ scripts/
└─ .github/
   └─ workflows/
```

## License
MIT

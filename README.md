# Network Latency Monitor

A latency monitoring service for tracking network performance across hosts.
Built with FastAPI and Docker.

## Stack

- Python 3.12
- FastAPI + uvicorn
- Docker + Docker Compose
- uv (dependency management)

## Quick start

```bash
docker compose up --build
```

Then:

```bash
curl http://localhost:8000/healthz
# {"status":"ok"}
```

## Local development

```bash
uv sync
uv run uvicorn net_monitor.main:app --reload
```

## Roadmap

- [x] Health check endpoint
- [ ] Ping target hosts and store results
- [ ] PostgreSQL persistence
- [ ] REST API for query results
- [ ] Prometheus metrics
- [ ] Grafana dashboard

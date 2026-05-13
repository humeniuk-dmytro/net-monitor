# Network Latency Monitor

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://net-monitor-1.onrender.com/docs)

[![CI](https://github.com/humeniuk-dmytro/net-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/humeniuk-dmytro/net-monitor/actions)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

> Monitor network latency to multiple hosts via REST API. Schedules ICMP pings, stores results in PostgreSQL, exposes stats endpoints.

## Why this project

Built to practice production-grade Python backend development: async FastAPI, SQLAlchemy 2.0, background scheduling, Docker Compose, and CI/CD.

## Stack

- Python 3.12 · FastAPI · PostgreSQL 16
- SQLAlchemy 2.0 + Alembic for migrations
- APScheduler for background pinging
- pytest · GitHub Actions CI
- Docker Compose for one-command setup

## Architecture

\`\`\`
Client → REST → FastAPI → PostgreSQL
                    ↑
              APScheduler (ping every 30s)
\`\`\`

## Quick start

\`\`\`bash
git clone https://github.com/humeniuk-dmytro/net-monitor
cd net-monitor
cp .env.example .env
docker compose up --build
\`\`\`

API available at http://localhost:8000/docs

Or try the live API: https://net-monitor-1.onrender.com/docs

## API examples

\`\`\`bash
# Add a host to monitor
curl -X POST http://localhost:8000/api/hosts \
  -H 'Content-Type: application/json' \
  -d '{"hostname": "8.8.8.8"}'

# Get latency stats for last hour
curl http://localhost:8000/api/hosts/1/stats\?period\=1h
\`\`\`

## Tests

\`\`\`bash
uv run pytest --cov=src/net_monitor
\`\`\`

## What I learned

- FastAPI lifespan events for background scheduler startup
- SQLAlchemy 2.0 async session management
- Alembic auto-generated migrations
- pytest fixtures for test database isolation
- Docker Compose multi-service orchestration

## License

MIT

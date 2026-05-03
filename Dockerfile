FROM python:3.12-slim

WORKDIR /app

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project metadata first (better layer caching)
COPY pyproject.toml uv.lock* README.md ./
COPY src/ ./src/

# Install only runtime deps
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "net_monitor.main:app", "--host", "0.0.0.0", "--port", "8000"]

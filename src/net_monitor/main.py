from fastapi import FastAPI

from net_monitor import __version__

app = FastAPI(title="Network Latency Monitor", version=__version__)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "net-monitor", "version": __version__}

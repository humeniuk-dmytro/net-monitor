from contextlib import asynccontextmanager
from fastapi import FastAPI
from net_monitor import __version__
from net_monitor.routers import hosts


@asynccontextmanager
async def lifespan(app: FastAPI):
    from net_monitor.scheduler import start_scheduler, stop_scheduler
    await start_scheduler()
    yield
    await stop_scheduler()


app = FastAPI(title="Network Latency Monitor", version=__version__, lifespan=lifespan)
app.include_router(hosts.router)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "net-monitor", "version": __version__}
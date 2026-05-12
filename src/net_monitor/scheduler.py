import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from net_monitor.database import AsyncSessionLocal
from net_monitor.models import Host, LatencyRecord
from net_monitor.pinger import ping_host

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def ping_all_hosts() -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Host).where(Host.is_active == True)  # noqa: E712
        )
        hosts = result.scalars().all()

    for host in hosts:
        latency_ms, status = await ping_host(host.hostname)
        logger.info("Pinged %s -> %s ms (%s)", host.hostname, latency_ms, status)
        async with AsyncSessionLocal() as db:
            db.add(LatencyRecord(
                host_id=host.id, latency_ms=latency_ms, status=status
            ))
            await db.commit()


async def start_scheduler() -> None:
    from net_monitor.config import get_settings
    s = get_settings()
    scheduler.add_job(ping_all_hosts, "interval", seconds=s.ping_interval_seconds)
    scheduler.start()
    logger.info("Scheduler started (interval=%ss)", s.ping_interval_seconds)


async def stop_scheduler() -> None:
    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")
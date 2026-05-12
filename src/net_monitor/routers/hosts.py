import statistics
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from net_monitor.database import get_db
from net_monitor.models import Host, LatencyRecord
from net_monitor.schemas import HostCreate, HostRead, StatsRead

router = APIRouter(prefix="/api/hosts", tags=["hosts"])


@router.post("", response_model=HostRead, status_code=201)
async def create_host(body: HostCreate, db: AsyncSession = Depends(get_db)):
    host = Host(hostname=body.hostname, ip=body.ip)
    db.add(host)
    await db.commit()
    await db.refresh(host)
    return host


@router.get("", response_model=list[HostRead])
async def list_hosts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Host).order_by(Host.id))
    return result.scalars().all()


@router.get("/{host_id}", response_model=HostRead)
async def get_host(host_id: int, db: AsyncSession = Depends(get_db)):
    host = await db.get(Host, host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    return host


@router.delete("/{host_id}", status_code=204)
async def delete_host(host_id: int, db: AsyncSession = Depends(get_db)):
    host = await db.get(Host, host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    await db.delete(host)
    await db.commit()


@router.get("/{host_id}/stats", response_model=StatsRead)
async def get_stats(host_id: int, period: str = "1h", db: AsyncSession = Depends(get_db)):
    host = await db.get(Host, host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    hours = {"1h": 1, "24h": 24, "7d": 168}.get(period, 1)
    since = datetime.utcnow() - timedelta(hours=hours)
    result = await db.execute(
        select(LatencyRecord)
        .where(LatencyRecord.host_id == host_id, LatencyRecord.timestamp >= since)
    )
    records = result.scalars().all()
    latencies = [r.latency_ms for r in records if r.latency_ms is not None]
    p95 = None
    if latencies:
        s = sorted(latencies)
        p95 = round(s[min(int(len(s)*0.95), len(s)-1)], 2)
    return StatsRead(
        host_id=host_id, period=period, count=len(records),
        avg_ms=round(statistics.mean(latencies), 2) if latencies else None,
        min_ms=min(latencies) if latencies else None,
        max_ms=max(latencies) if latencies else None,
        p95_ms=p95,
    )
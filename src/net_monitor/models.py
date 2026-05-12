from datetime import datetime
from sqlalchemy import ForeignKey, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from net_monitor.database import Base


class Host(Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    records: Mapped[list["LatencyRecord"]] = relationship(back_populates="host")


class LatencyRecord(Base):
    __tablename__ = "latency_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("hosts.id", ondelete="CASCADE"))
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ok")
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    host: Mapped["Host"] = relationship(back_populates="records")
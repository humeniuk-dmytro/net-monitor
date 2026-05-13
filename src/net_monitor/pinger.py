import asyncio
import re
import socket


async def ping_host(hostname: str) -> tuple[float | None, str]:
    """Ping a host once. Returns (latency_ms, status)."""
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        return None, "error"
    try:
        proc = await asyncio.create_subprocess_exec(
            "ping", "-c", "1", "-W", "2", ip,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=5)
        output = stdout.decode()
        match = re.search(r"time[=<]([\d.]+)\s*ms", output)
        if proc.returncode == 0 and match:
            return float(match.group(1)), "ok"
        return None, "timeout"
    except asyncio.TimeoutError:
        return None, "timeout"
    except Exception:
        return None, "error"
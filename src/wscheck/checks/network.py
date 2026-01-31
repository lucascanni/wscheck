import socket
import time

import requests


def _dns_ok(host: str = "google.com") -> bool:
    """
    Resolve a hostname to check DNS availability.
    """
    try:
        socket.gethostbyname(host)
        return True
    except OSError:
        return False


def _tcp_latency_ms(host: str, port: int, timeout: float = 2.0) -> float | None:
    """
    Measure connectivity/latency by attempting a TCP connection.
    Returns latency in milliseconds, or None if it fails.
    """
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return round((time.time() - start) * 1000, 1)
    except OSError:
        return None


def _http_ok(url: str = "https://www.google.com", timeout: float = 3.0) -> bool:
    """
    Perform a simple HTTP GET to verify internet access.
    """
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code < 500
    except requests.RequestException:
        return False


def collect_network() -> dict:
    """
    Collect basic network health metrics.

    Returns:
        dict: DNS status, TCP latency and HTTP reachability with a status label
    """
    dns_ok = _dns_ok("google.com")

    latency_ms = _tcp_latency_ms("1.1.1.1", 53, timeout=2.0)  

    http_ok = _http_ok("https://www.google.com", timeout=3.0)

    status = "OK"
    if not dns_ok and not http_ok:
        status = "CRITICAL"
    elif (not dns_ok) or (latency_ms is None) or (not http_ok):
        status = "WARNING"

    return {
        "dns_ok": dns_ok,
        "tcp_latency_ms": latency_ms if latency_ms is not None else "N/A",
        "http_ok": http_ok,
        "status": status,
    }

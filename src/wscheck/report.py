import csv
import json
from pathlib import Path


def export_json(data: dict, path: Path) -> None:
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def export_csv(data: dict, path: Path) -> None:
    
    path.parent.mkdir(parents=True, exist_ok=True)

    sysd = data.get("system", {})
    netd = data.get("network", {})
    svcd = data.get("services", {})
    health = data.get("health", {})

    fields = [
        "hostname",
        "os",
        "cpu_percent",
        "ram_percent",
        "disk_percent",
        "dns_ok",
        "http_ok",
        "tcp_latency_ms",
        "profile",
        "missing_processes",
        "score",
        "status",
    ]

    row = {
        "hostname": sysd.get("hostname", ""),
        "os": sysd.get("os", ""),
        "cpu_percent": sysd.get("cpu_percent", ""),
        "ram_percent": sysd.get("ram_percent", ""),
        "disk_percent": sysd.get("disk_percent", ""),
        "dns_ok": netd.get("dns_ok", ""),
        "http_ok": netd.get("http_ok", ""),
        "tcp_latency_ms": netd.get("tcp_latency_ms", ""),
        "profile": svcd.get("profile", ""),
        "missing_processes": ", ".join(svcd.get("missing", []) or []),
        "score": health.get("score", ""),
        "status": health.get("status", ""),
    }

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)

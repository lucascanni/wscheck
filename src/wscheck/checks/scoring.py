def compute_health(data: dict) -> dict:
    
    score = 100
    issues: list[str] = []

    sysd = data.get("system", {})
    netd = data.get("network", {})
    svcd = data.get("services", {})

    cpu = float(sysd.get("cpu_percent", 0))
    ram = float(sysd.get("ram_percent", 0))
    disk = float(sysd.get("disk_percent", 0))

    if cpu > 75:
        score -= 10
        issues.append("High CPU usage")
    if ram > 80:
        score -= 10
        issues.append("High RAM usage")
    if disk > 90:
        score -= 15
        issues.append("Low disk space")

    dns_ok = bool(netd.get("dns_ok", True))
    http_ok = bool(netd.get("http_ok", True))
    latency = netd.get("tcp_latency_ms", "N/A")

    if not dns_ok:
        score -= 20
        issues.append("DNS resolution failed")
    if not http_ok:
        score -= 15
        issues.append("HTTP connectivity failed")
    if latency == "N/A":
        score -= 10
        issues.append("TCP connectivity/latency unavailable")

    missing = svcd.get("missing", [])
    if missing:
        penalty = min(20, 5 * len(missing))
        score -= penalty
        issues.append("Missing processes: " + ", ".join(missing))

    score = max(0, min(100, score))

    status = "OK"
    if score < 60:
        status = "CRITICAL"
    elif score < 80:
        status = "WARNING"

    return {"score": score, "status": status, "issues": issues}

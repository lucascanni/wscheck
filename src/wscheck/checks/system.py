import os
import platform
import socket
import time

import psutil


def _system_drive() -> str:
    
    return os.environ.get("SystemDrive", "C:") + "\\"


def collect_system() -> dict:
    
    cpu_percent = psutil.cpu_percent(interval=0.6)
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage(_system_drive()).percent

    uptime_seconds = int(time.time() - psutil.boot_time())

    # Determine system status based on thresholds
    status = "OK"
    if cpu_percent > 90 or ram_percent > 90 or disk_percent > 95:
        status = "CRITICAL"
    elif cpu_percent > 75 or ram_percent > 80 or disk_percent > 90:
        status = "WARNING"

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_percent": round(cpu_percent, 1),
        "ram_percent": round(ram_percent, 1),
        "disk_percent": round(disk_percent, 1),
        "system_drive": _system_drive(),
        "uptime_seconds": uptime_seconds,
        "status": status,
    }

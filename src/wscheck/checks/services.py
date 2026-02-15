import psutil

PROCESS_PROFILES: dict[str, list[str]] = {
    "generic": [
        "OneDrive.exe",
        "Teams.exe",
        "chrome.exe",
    ],
    "office": [
        "OneDrive.exe",
        "Teams.exe",
        "chrome.exe",
    ],
    "dev": [
        "Code.exe",
        "python.exe",
    ],
}


def collect_services(profile: str = "generic") -> dict:
    
    expected = PROCESS_PROFILES.get(profile, PROCESS_PROFILES["generic"])

    running_names: set[str] = set()
    for proc in psutil.process_iter(attrs=["name"]):
        name = (proc.info.get("name") or "").lower()
        if name:
            running_names.add(name)

    found: list[str] = []
    missing: list[str] = []

    for proc_name in expected:
        needle = proc_name.lower()
        if any(needle in running for running in running_names):
            found.append(proc_name)
        else:
            missing.append(proc_name)

    status = "OK"
    if len(expected) > 0 and len(missing) == len(expected):
        status = "CRITICAL"
    elif missing:
        status = "WARNING"

    return {
        "profile": profile,
        "expected": expected,
        "running_count": len(found),
        "expected_count": len(expected),
        "missing": missing,
        "status": status,
    }

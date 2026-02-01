import psutil

DEFAULT_EXPECTED_PROCESSES = [
    "OneDrive.exe",
    "Teams.exe",
    "Code.exe",
    "chrome.exe",
    "python.exe",
]


def collect_services(expected: list[str] | None = None) -> dict:
    """
    Check whether expected processes are currently running.

    Args:
        expected: list of process names to look for (case-insensitive)

    Returns:
        dict: running/missing processes + status label
    """
    expected = expected or DEFAULT_EXPECTED_PROCESSES

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
        "expected": expected,
        "running_count": len(found),
        "expected_count": len(expected),
        "missing": missing,
        "status": status,
    }

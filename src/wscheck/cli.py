import typer

from wscheck.checks.system import collect_system

app = typer.Typer(help="wscheck - Workstation Health Check CLI")


@app.callback()
def main():
    """
    CLI tool to diagnose the health of a Windows workstation.
    """
    pass


@app.command("hello")
def hello():
    """
    Test command to verify the CLI is working.
    """
    print("wscheck ready")


def _print_system_report(system: dict) -> None:
    """
    Print system health data in a readable, multi-line format.
    """
    print("\nSystem Health Check")
    print("-" * 30)

    for key, value in system.items():
        print(f"{key:20} : {value}")


@app.command("scan")
def scan():
    """
    Run a workstation health check (system metrics only - v1).
    """
    system_data = collect_system()
    _print_system_report(system_data)

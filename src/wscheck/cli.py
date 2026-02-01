import typer

from wscheck.checks.system import collect_system
from wscheck.checks.network import collect_network
from wscheck.checks.services import collect_services, PROCESS_PROFILES
from wscheck.checks.scoring import compute_health
from wscheck.report import export_json, export_csv

from datetime import datetime
from pathlib import Path

app = typer.Typer(help="wscheck - Workstation Health Check CLI")


@app.callback()
def main():
    """
    CLI tool to diagnose the health of a Windows workstation.
    """
    pass

@app.command("test")
def test():
    """
    Test command to verify the CLI is working.
    """
    print("wscheck ready")

def _print_section(title: str, data: dict) -> None:
    """
    Print a section (title + key/value pairs) in a readable multi-line format.
    """
    print(f"\n{title}")
    print("-" * len(title))
    for key, value in data.items():
        print(f"{key:20} : {value}")


@app.command("scan")
def scan(
    profile: str = typer.Option(
        "generic",
        help="Workstation profile: generic | office | dev",
        case_sensitive=False,
    ),
    export: str = typer.Option(
        "none",
        help="Export format: none | json | csv | both",
        case_sensitive=False,
    ),
):
    """
    Run a workstation health check using a specific profile.
    """
    if profile not in PROCESS_PROFILES:
        typer.echo(f"Unknown profile '{profile}'. Available profiles:")
        for p in PROCESS_PROFILES:
            typer.echo(f"  - {p}")
        raise typer.Exit(code=2)

    system_data = collect_system()
    network_data = collect_network()
    services_data = collect_services(profile=profile)

    data = {
        "system": system_data,
        "network": network_data,
        "services": services_data,
    }

    global_health = compute_health(data)
    data["health"] = global_health

    _print_section("System Health Check", system_data)
    _print_section("Network Health Check", network_data)
    _print_section("Services / Processes Check", services_data)
    _print_section("Global Health", global_health)

    report_dir = Path("data/reports")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if export in ("json", "both"):
        json_path = report_dir / f"wscheck_report_{timestamp}.json"
        export_json(data, json_path)
        typer.echo(f"Exported JSON -> {json_path}")

    if export in ("csv", "both"):
        csv_path = report_dir / f"wscheck_report_{timestamp}.csv"
        export_csv(data, csv_path)
        typer.echo(f"Exported CSV  -> {csv_path}")


    if global_health["status"] == "CRITICAL":
        raise typer.Exit(code=2)
    if global_health["status"] == "WARNING":
        raise typer.Exit(code=1)

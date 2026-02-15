import typer
import json

from wscheck.checks.system import collect_system
from wscheck.checks.network import collect_network
from wscheck.checks.services import collect_services, PROCESS_PROFILES
from wscheck.checks.scoring import compute_health
from wscheck.report import export_json, export_csv
from wscheck.logger import get_logger
from wscheck import __version__

from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table


app = typer.Typer(
    help="wscheck - Workstation Health Check CLI",
    add_completion=False,
)
console = Console()
logger = get_logger()

@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        help="Show installed version.",
        is_eager=True,
    )
):
    """
    CLI tool to diagnose the health of a Windows workstation.
    """
    if version:
        typer.echo(f"wscheck {__version__}")
        raise typer.Exit()
    return

def _render_rich_report(data: dict) -> None:
    """
    Render the scan results in a Rich table.
    """
    sysd = data.get("system", {})
    netd = data.get("network", {})
    svcd = data.get("services", {})
    health = data.get("health", {})

    table = Table(title="Workstation Health Check")

    table.add_column("Category", style="bold")
    table.add_column("Summary")
    table.add_column("Status", style="bold")

    table.add_row(
        "System",
        f"CPU {sysd.get('cpu_percent')}% | RAM {sysd.get('ram_percent')}% | Disk {sysd.get('disk_percent')}% ({sysd.get('system_drive')})",
        str(sysd.get("status")),
    )

    table.add_row(
        "Network",
        f"DNS {netd.get('dns_ok')} | HTTP {netd.get('http_ok')} | TCP latency {netd.get('tcp_latency_ms')}ms",
        str(netd.get("status")),
    )

    missing = svcd.get("missing", []) or []
    table.add_row(
        "Services",
        f"Profile {svcd.get('profile')} | Running {svcd.get('running_count')}/{svcd.get('expected_count')} | Missing: {', '.join(missing) if missing else 'None'}",
        str(svcd.get("status")),
    )

    issues = health.get("issues", []) or []
    table.add_row(
        "Global",
        f"Score {health.get('score')}/100 | Issues: {', '.join(issues) if issues else 'None'}",
        str(health.get("status")),
    )

    console.print(table)

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
    pretty: bool = typer.Option(
        True,
        help="Pretty terminal output (Rich table). Disable for plain text output.",
    ),
    output: str = typer.Option(
        "text",
        help="Output format to STDOUT: text | json",
        case_sensitive=False,
    ),
    verbose: bool = typer.Option(
        False,
        help="Enable verbose logging.",
    ),
):
    """
    Run a workstation health check using a specific profile.
    """
    if verbose:
        logger.setLevel("DEBUG")

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
    logger.info("Scan started | profile=%s", profile)
    logger.info("System status=%s | CPU=%s RAM=%s DISK=%s",
                system_data.get("status"),
                system_data.get("cpu_percent"),
                system_data.get("ram_percent"),
                system_data.get("disk_percent"))

    logger.info("Network status=%s | DNS=%s HTTP=%s LAT=%s",
                network_data.get("status"),
                network_data.get("dns_ok"),
                network_data.get("http_ok"),
                network_data.get("tcp_latency_ms"))

    logger.info("Services status=%s | missing=%s",
                services_data.get("status"),
                ", ".join(services_data.get("missing", []) or []) or "None")

    logger.info("Global status=%s | score=%s | issues=%s",
                global_health.get("status"),
                global_health.get("score"),
                ", ".join(global_health.get("issues", []) or []) or "None")


    if output == "json":
        typer.echo(json.dumps(data, indent=2))
        if global_health["status"] == "CRITICAL":
            raise typer.Exit(code=2)
        if global_health["status"] == "WARNING":
            raise typer.Exit(code=1)
        return

    if pretty:
        _render_rich_report(data)
    else:
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
        logger.info("Exported JSON report -> %s", json_path)

    if export in ("csv", "both"):
        csv_path = report_dir / f"wscheck_report_{timestamp}.csv"
        export_csv(data, csv_path)
        typer.echo(f"Exported CSV  -> {csv_path}")
        logger.info("Exported CSV report -> %s", csv_path)


    if global_health["status"] == "CRITICAL":
        raise typer.Exit(code=2)
    if global_health["status"] == "WARNING":
        raise typer.Exit(code=1)

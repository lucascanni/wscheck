#  wscheck

`wscheck` is a Python CLI tool designed to assess the health of a Windows workstation.

It performs system, network, and process checks, computes a global health score, and provides automation-ready outputs and reports.

---

#  Features (v1)

##  System Checks

- CPU usage
- RAM usage
- Disk usage (system drive)
- Hostname & OS version
- Uptime
- Status (OK / WARNING / CRITICAL)

##  Network Checks

- DNS resolution test
- TCP connectivity test
- HTTP reachability test
- Network status evaluation

##  Services / Process Checks

Profile-based validation:

- `generic`
- `office`
- `dev`

Checks for expected running processes.

##  Global Health Scoring

- Score from 0 to 100
- Aggregated status
- List of detected issues

##  Reports

- JSON export
- CSV export (Excel-friendly)
- Timestamped filenames
- Logs saved to file

##  Automation Ready

### Exit Codes

| Code | Meaning    |
|------|------------|
| 0    | OK         |
| 1    | WARNING    |
| 2    | CRITICAL   |

### Additional Automation Features

- JSON output to STDOUT (`--output json`)
- Structured logging (`data/reports/wscheck.log`)


##  Terminal Output

- Rich table (default)
- Plain text fallback (`--no-pretty`)

##  Versioning

```powershell
wscheck --version
```

#  Project Structure

    src/wscheck/
    │
    ├── __init__.py
    ├── cli.py
    ├── logger.py
    ├── report.py
    └── checks/
        ├── system.py
        ├── network.py
        ├── services.py
        └── scoring.py

Reports and logs are stored in:

    data/reports/

# 📦 Installation

## 1️⃣ Clone repository

``` bash
git clone https://github.com/yourusername/wscheck.git
cd wscheck
```

## 2️⃣ Create virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3️⃣ Install project

``` powershell
pip install -e .
```

# 🧪 Usage

## Basic scan

``` powershell
wscheck scan
```

## Select profile

``` powershell
wscheck scan --profile generic
wscheck scan --profile office
wscheck scan --profile dev
```

### Available profiles

-   `generic`
-   `office`
-   `dev`

# 📤 Export Reports

``` powershell
wscheck scan --export json
wscheck scan --export csv
wscheck scan --export both
```

Reports are stored in:

    data/reports/

Example filename:

    wscheck_report_2026-02-15_14-32-10.json

------------------------------------------------------------------------

# 📦 Output to JSON (STDOUT)

Useful for scripting and automation:

``` powershell
wscheck scan --output json
```

Example usage in PowerShell:

``` powershell
wscheck scan --output json | Out-File report.json
```

------------------------------------------------------------------------

# 🎨 Terminal Display Modes

## Rich table (default)

``` powershell
wscheck scan
```

## Plain text

``` powershell
wscheck scan --no-pretty
```

# 🔢 Exit Codes

  Code   Meaning
  ------ ----------
  0      OK
  1      WARNING
  2      CRITICAL

Example:

``` powershell
wscheck scan
echo $LASTEXITCODE
```

# 📝 Logging

Logs are written to:

    data/reports/wscheck.log

Each scan logs:

-   Profile used
-   System metrics
-   Network status
-   Services status
-   Global score
-   Exported files

Enable verbose mode:

``` powershell
wscheck scan --verbose
```

# ⚙️ Profiles

Profiles define which processes must be running.

## generic

-   OneDrive
-   Teams
-   Chrome browser

## office

-   OneDrive
-   Teams
-   Chrome browser

## dev

-   VS Code
-   Python

Profiles can be extended in:

    checks/services.py

# 📈 Example Output

    ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Category  ┃ Summary                              ┃ Status   ┃
    ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ System    │ CPU 9.2% | RAM 68.1% | Disk 41% (C:\)│ OK       │
    │ Network   │ DNS True | HTTP True | TCP 40.8ms    │ OK       │
    │ Services  │ Profile office | Running 3/3         │ OK       │
    │ Global    │ Score 100/100 | Issues: None         │ OK       │
    └───────────┴──────────────────────────────────────┴──────────┘

# 🎯 Use Cases

-   IT support diagnostics
-   Pre-deployment validation
-   Remote workstation validation
-   Basic health monitoring
-   Integration with automation scripts
-   Educational CLI architecture example

# 🔐 Safety

-   Read-only checks (no destructive operations)
-   No elevation required
-   No external telemetry
-   Local-only analysis

# 🧑‍💻 Author

Built as an IT automation and system diagnostics tool.

# 🚀 Roadmap (v2 ideas)

-   Config file support (YAML/JSON)
-   Baseline comparison
-   Scheduled monitoring mode
-   HTML report export
-   Unit tests (pytest)
-   CI pipeline
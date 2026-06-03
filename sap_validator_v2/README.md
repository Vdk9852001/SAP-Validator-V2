# SAP Migration Post-Load Validator

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the dashboard
python dashboard/app.py

# 3. Open browser
http://localhost:5000
```

## How to use

1. Drop your **source CSV/XLSX** files into  `data/source/`
2. Drop your **target CSV/XLSX** files into  `data/target/`
3. Files are matched by name — `MATERIAL.csv` pairs with `MATERIAL.csv`
4. Dashboard auto-scans every 10 seconds — or click "Scan Now"

## What it validates

- Record count comparison (source vs target)
- Key matching (which records exist in both / only one side)
- Every field that exists in both files — auto-detected
- Numeric columns auto-detected from data — no hardcoding
- Tolerances auto-scaled from the magnitude of each numeric column

## Folder structure

```
sap_validator/
  core/
    validator.py        <- validation engine
  dashboard/
    app.py              <- Flask web server
    templates/
      dashboard.html    <- dashboard UI
  data/
    source/             <- DROP SOURCE FILES HERE
    target/             <- DROP TARGET FILES HERE
  requirements.txt
  README.md
```

## CLI (optional, no dashboard)

```bash
python validate.py --source data/source/MATERIAL.csv --target data/target/MATERIAL.csv
```

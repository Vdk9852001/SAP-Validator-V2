"""
SAP Migration Post-Load Validator - Live Dashboard
Run:  python dashboard/app.py
Open: http://localhost:5000

Drop source files into: data/source/
Drop target files into: data/target/
Files are matched by name: MATERIAL.csv <-> MATERIAL.csv
Excel reports are saved to: reports/<TABLE>_<timestamp>.xlsx
"""

import sys
import threading
import time
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, send_file

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.validator import MaterialValidator
from core.reporter import generate_excel_report

app = Flask(__name__)

BASE_DIR    = Path(__file__).parent.parent
SOURCE_DIR  = BASE_DIR / "data" / "source"
TARGET_DIR  = BASE_DIR / "data" / "target"
REPORTS_DIR = BASE_DIR / "reports"
SOURCE_DIR.mkdir(parents=True, exist_ok=True)
TARGET_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

results_store = {}   # name -> result dict
scan_status   = {"last_scan": None, "scanning": False, "error": None}
SUPPORTED_EXT = {".csv", ".xlsx", ".xls"}


# ── File discovery ────────────────────────────────────────────────────────────
def discover_pairs():
    src_files = {
        f.stem.upper(): f
        for f in SOURCE_DIR.iterdir()
        if f.suffix.lower() in SUPPORTED_EXT
    }
    tgt_files = {
        f.stem.upper(): f
        for f in TARGET_DIR.iterdir()
        if f.suffix.lower() in SUPPORTED_EXT
    }
    all_names = sorted(set(src_files) | set(tgt_files))
    pairs = []
    for name in all_names:
        pairs.append({
            "name":        name,
            "source_path": str(src_files[name]) if name in src_files else None,
            "target_path": str(tgt_files[name]) if name in tgt_files else None,
            "has_pair":    name in src_files and name in tgt_files,
        })
    return pairs


# ── Validation runner ─────────────────────────────────────────────────────────
def run_validation(name, source_path, target_path):
    validator = MaterialValidator()
    result    = validator.validate(source_path, target_path)
    ss        = result.summary_stats

    field_rows = []
    for fr in result.field_results:
        field_rows.append({
            "field":        fr.field_source,
            "field_target": fr.field_target,
            "type":         "numeric" if fr.is_numeric else "string",
            "tolerance":    fr.tolerance_used,
            "total":        fr.total_records,
            "matched":      fr.matched,
            "mismatched":   fr.mismatched,
            "miss_source":  fr.missing_in_source,
            "miss_target":  fr.missing_in_target,
            "match_pct":    fr.match_pct,
            "status":       fr.status,
            "mismatches":   fr.mismatch_details[:50],
        })

    mapping = None
    if result.mapping:
        mapping = {
            "join_key":           result.mapping.join_key,
            "matched_fields":     result.mapping.matched_fields,
            "source_only_fields": result.mapping.source_only_fields,
            "target_only_fields": result.mapping.target_only_fields,
            "numeric_fields":     result.mapping.numeric_fields,
            "tolerance_map":      result.mapping.tolerance_map,
        }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"{name}_{ts}.xlsx"
    excel_path     = REPORTS_DIR / excel_filename

    result_dict = {
        "name":                   name,
        "status":                 result.overall_status,
        "source_file":            Path(source_path).name,
        "target_file":            Path(target_path).name,
        "total_source_records":   result.total_source_records,
        "total_target_records":   result.total_target_records,
        "records_matched":        result.records_matched,
        "records_only_in_source": result.records_only_in_source,
        "records_only_in_target": result.records_only_in_target,
        "fields_passed":          ss["fields_passed"],
        "fields_failed":          ss["fields_failed"],
        "total_fields":           ss["total_fields_validated"],
        "pass_rate_pct":          ss["pass_rate_pct"],
        "errors":                 result.errors,
        "mapping":                mapping,
        "field_results":          field_rows,
        "run_at":                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "excel_file":             excel_filename,   # stored for download link
    }

    # Generate Excel report
    try:
        generate_excel_report(result_dict, str(excel_path))
    except Exception as e:
        result_dict["excel_error"] = str(e)

    return result_dict


def scan_and_validate_all():
    scan_status["scanning"] = True
    scan_status["error"]    = None
    try:
        pairs = discover_pairs()
        for pair in pairs:
            if not pair["has_pair"]:
                continue
            name       = pair["name"]
            src_mtime  = Path(pair["source_path"]).stat().st_mtime
            tgt_mtime  = Path(pair["target_path"]).stat().st_mtime
            last_mtime = max(src_mtime, tgt_mtime)
            existing   = results_store.get(name)
            if existing and existing.get("_mtime") == last_mtime:
                continue   # unchanged — skip
            result = run_validation(name, pair["source_path"], pair["target_path"])
            result["_mtime"] = last_mtime
            results_store[name] = result
        scan_status["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        scan_status["error"] = str(e)
    finally:
        scan_status["scanning"] = False


def background_watcher(interval=10):
    while True:
        scan_and_validate_all()
        time.sleep(interval)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/scan", methods=["POST"])
def api_scan():
    threading.Thread(target=scan_and_validate_all, daemon=True).start()
    return jsonify({"ok": True})

@app.route("/api/status")
def api_status():
    pairs = discover_pairs()
    return jsonify({
        "last_scan":    scan_status["last_scan"],
        "scanning":     scan_status["scanning"],
        "error":        scan_status["error"],
        "source_dir":   str(SOURCE_DIR),
        "target_dir":   str(TARGET_DIR),
        "pairs":        pairs,
        "total_tables": len([p for p in pairs if p["has_pair"]]),
        "unmatched":    len([p for p in pairs if not p["has_pair"]]),
    })

@app.route("/api/results")
def api_results():
    return jsonify(list(results_store.values()))

@app.route("/api/results/<name>")
def api_result_detail(name):
    result = results_store.get(name.upper())
    if not result:
        return jsonify({"error": "Not found"}), 404
    return jsonify(result)

@app.route("/api/download/<name>")
def api_download(name):
    """Download the Excel report for a table."""
    result = results_store.get(name.upper())
    if not result:
        return jsonify({"error": "Not found"}), 404
    excel_file = result.get("excel_file")
    if not excel_file:
        return jsonify({"error": "No Excel report available"}), 404
    path = REPORTS_DIR / excel_file
    if not path.exists():
        return jsonify({"error": "Report file missing — re-run scan"}), 404
    return send_file(
        str(path),
        as_attachment=True,
        download_name=excel_file,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/api/download-file/<filename>")
def api_download_file(filename):
    """Download any Excel report by filename (used by reports modal)."""
    path = REPORTS_DIR / filename
    if not path.exists() or not filename.endswith(".xlsx"):
        return jsonify({"error": "File not found"}), 404
    return send_file(
        str(path),
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/api/reports")
def api_reports():
    """List all saved Excel reports."""
    files = sorted(REPORTS_DIR.glob("*.xlsx"), key=lambda f: f.stat().st_mtime, reverse=True)
    return jsonify([
        {"filename": f.name, "size_kb": round(f.stat().st_size / 1024, 1),
         "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")}
        for f in files
    ])

@app.route("/api/folders")
def api_folders():
    return jsonify({
        "source_dir": str(SOURCE_DIR),
        "target_dir": str(TARGET_DIR),
        "reports_dir": str(REPORTS_DIR),
    })


if __name__ == "__main__":
    print(f"\n  SAP Post-Load Validator - Dashboard")
    print(f"  Drop source files -> {SOURCE_DIR}")
    print(f"  Drop target files -> {TARGET_DIR}")
    print(f"  Excel reports     -> {REPORTS_DIR}")
    print(f"  Open              -> http://localhost:5000\n")
    threading.Thread(target=scan_and_validate_all, daemon=True).start()
    threading.Thread(target=background_watcher, args=(10,), daemon=True).start()
    app.run(debug=False, port=5000, use_reloader=False)

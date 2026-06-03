"""
SAP Migration Post-Load Validator - Live Dashboard
Run:  python dashboard/app.py
Open: http://localhost:5000

Drop source files into: data/source/
Drop target files into: data/target/
Files matched by name: MATERIAL.csv <-> MATERIAL.csv
Excel reports saved to: reports/<TABLE>_<timestamp>.xlsx
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

results_store = {}
scan_status   = {"last_scan": None, "scanning": False, "error": None}
file_states   = {}   # name -> {state, detected_at, source_file, target_file}
activity_log  = []   # last 50 events
SUPPORTED_EXT = {".csv", ".xlsx", ".xls"}


def log_event(message, level="info"):
    entry = {
        "ts":      datetime.now().strftime("%H:%M:%S"),
        "message": message,
        "level":   level,
    }
    activity_log.append(entry)
    if len(activity_log) > 50:
        activity_log.pop(0)
    print(f"  [{entry['ts']}] {message}")


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
        src_path = str(src_files[name]) if name in src_files else None
        tgt_path = str(tgt_files[name]) if name in tgt_files else None
        has_pair = name in src_files and name in tgt_files
        mtime = None
        if has_pair:
            mtime = max(
                Path(src_path).stat().st_mtime,
                Path(tgt_path).stat().st_mtime
            )
        pairs.append({
            "name":        name,
            "source_path": src_path,
            "target_path": tgt_path,
            "has_pair":    has_pair,
            "mtime":       mtime,
            "source_file": Path(src_path).name if src_path else None,
            "target_file": Path(tgt_path).name if tgt_path else None,
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

    ts             = datetime.now().strftime("%Y%m%d_%H%M%S")
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
        "excel_file":             excel_filename,
    }

    try:
        generate_excel_report(result_dict, str(excel_path))
    except Exception as e:
        result_dict["excel_error"] = str(e)
        log_event(f"Excel generation failed for {name}: {e}", "error")

    return result_dict


def scan_and_validate_all():
    scan_status["scanning"] = True
    scan_status["error"]    = None
    try:
        pairs = discover_pairs()

        for pair in pairs:
            name = pair["name"]

            if not pair["has_pair"]:
                prev = file_states.get(name, {})
                if prev.get("state") != "unmatched":
                    side = "source" if pair["source_path"] else "target"
                    other = "target" if side == "source" else "source"
                    log_event(
                        f"{name}: found in {side} only — waiting for matching {other} file",
                        "warn"
                    )
                    file_states[name] = {
                        "state":       "unmatched",
                        "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_file": pair["source_file"],
                        "target_file": pair["target_file"],
                    }
                continue

            last_mtime = pair["mtime"]
            existing   = results_store.get(name)
            prev_state = file_states.get(name, {})

            if not existing:
                log_event(
                    f"{name}: new file pair detected — "
                    f"{pair['source_file']} + {pair['target_file']}",
                    "info"
                )
            elif prev_state.get("_mtime") != last_mtime:
                log_event(f"{name}: file change detected — re-validating", "info")
            else:
                continue  # unchanged

            file_states[name] = {
                "state":       "validating",
                "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_file": pair["source_file"],
                "target_file": pair["target_file"],
                "_mtime":      last_mtime,
            }

            try:
                result = run_validation(name, pair["source_path"], pair["target_path"])
                result["_mtime"] = last_mtime
                results_store[name] = result

                file_states[name] = {
                    "state":        "done",
                    "detected_at":  file_states[name]["detected_at"],
                    "validated_at": result["run_at"],
                    "source_file":  pair["source_file"],
                    "target_file":  pair["target_file"],
                    "_mtime":       last_mtime,
                }

                level = "success" if result["status"] == "PASS" else "warn"
                log_event(
                    f"{name}: validation complete — {result['status']} "
                    f"({result['fields_passed']}/{result['total_fields']} fields passed, "
                    f"{result['records_matched']:,} records matched)",
                    level
                )

            except Exception as e:
                file_states[name]["state"] = "error"
                log_event(f"{name}: validation error — {e}", "error")

        scan_status["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        scan_status["error"] = str(e)
        log_event(f"Scan error: {e}", "error")
    finally:
        scan_status["scanning"] = False


def background_watcher(interval=5):
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
        "file_states":  file_states,
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

@app.route("/api/activity")
def api_activity():
    return jsonify(list(reversed(activity_log)))

@app.route("/api/download/<name>")
def api_download(name):
    result = results_store.get(name.upper())
    if not result:
        return jsonify({"error": "Not found"}), 404
    excel_file = result.get("excel_file")
    if not excel_file:
        return jsonify({"error": "No Excel report available"}), 404
    path = REPORTS_DIR / excel_file
    if not path.exists():
        return jsonify({"error": "Report file missing — re-run scan"}), 404
    return send_file(str(path), as_attachment=True, download_name=excel_file,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.route("/api/download-file/<filename>")
def api_download_file(filename):
    path = REPORTS_DIR / filename
    if not path.exists() or not filename.endswith(".xlsx"):
        return jsonify({"error": "File not found"}), 404
    return send_file(str(path), as_attachment=True, download_name=filename,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.route("/api/reports")
def api_reports():
    files = sorted(REPORTS_DIR.glob("*.xlsx"), key=lambda f: f.stat().st_mtime, reverse=True)
    return jsonify([
        {"filename": f.name, "size_kb": round(f.stat().st_size / 1024, 1),
         "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")}
        for f in files
    ])

@app.route("/api/folders")
def api_folders():
    return jsonify({
        "source_dir":  str(SOURCE_DIR),
        "target_dir":  str(TARGET_DIR),
        "reports_dir": str(REPORTS_DIR),
    })


if __name__ == "__main__":
    print(f"\n  SAP Post-Load Validator - Dashboard")
    print(f"  Drop source files -> {SOURCE_DIR}")
    print(f"  Drop target files -> {TARGET_DIR}")
    print(f"  Excel reports     -> {REPORTS_DIR}")
    print(f"  Open              -> http://localhost:5000\n")
    threading.Thread(target=scan_and_validate_all, daemon=True).start()
    threading.Thread(target=background_watcher, args=(5,), daemon=True).start()
    app.run(debug=False, port=5000, use_reloader=False)

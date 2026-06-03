<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAP Migration Validator</title>
<style>
  *, *::before, *::after { box-sizing:border-box; margin:0; padding:0; }
  :root {
    --bg:#0f1117; --surface:#1a1d27; --surface2:#222536;
    --border:#2e3248; --text:#e2e4f0; --muted:#7c82a0;
    --pass:#22c55e; --fail:#ef4444; --warn:#f59e0b;
    --info:#3b82f6; --accent:#6366f1;
  }
  body { font-family:'Segoe UI',system-ui,sans-serif;
         background:var(--bg); color:var(--text); min-height:100vh; }

  header { background:var(--surface); border-bottom:1px solid var(--border);
           padding:0 28px; display:flex; align-items:center;
           justify-content:space-between; height:56px; }
  .logo  { font-size:15px; font-weight:600; display:flex; align-items:center; gap:10px; }
  .logo span { color:var(--accent); }
  .header-right { display:flex; align-items:center; gap:10px; }
  .hbtn { border:none; padding:7px 16px; border-radius:6px; font-size:13px;
          cursor:pointer; font-weight:500; transition:opacity .2s; }
  #scan-btn    { background:var(--accent); color:#fff; }
  #reports-btn { background:var(--surface2); color:var(--text); border:1px solid var(--border); }
  #log-btn     { background:var(--surface2); color:var(--text); border:1px solid var(--border); }
  .hbtn:hover    { opacity:.85; }
  .hbtn:disabled { opacity:.4; cursor:default; }
  .last-scan { font-size:12px; color:var(--muted); }

  .layout { display:grid; grid-template-columns:280px 1fr;
            height:calc(100vh - 56px); }

  aside { background:var(--surface); border-right:1px solid var(--border);
          display:flex; flex-direction:column; overflow:hidden; }
  .sidebar-head { padding:16px 18px 10px; font-size:11px; font-weight:600;
                  color:var(--muted); letter-spacing:.06em; text-transform:uppercase; }
  #table-list { flex:1; overflow-y:auto; }
  .table-item { display:flex; align-items:center; justify-content:space-between;
                padding:10px 18px; cursor:pointer; border-left:3px solid transparent;
                transition:background .15s; font-size:13px; gap:8px; }
  .table-item:hover  { background:var(--surface2); }
  .table-item.active { background:var(--surface2); border-left-color:var(--accent); }
  .tname { font-weight:500; flex:1; min-width:0;
           white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

  .state-pill { font-size:10px; font-weight:700; padding:2px 7px;
                border-radius:10px; flex-shrink:0; white-space:nowrap; }
  .state-new        { background:rgba(59,130,246,.2);  color:#60a5fa; }
  .state-changed    { background:rgba(245,158,11,.2);  color:var(--warn); }
  .state-validating { background:rgba(99,102,241,.2);  color:#a5b4fc;
                      animation:blink .8s ease-in-out infinite; }
  .state-done-pass  { background:rgba(34,197,94,.15);  color:var(--pass); }
  .state-done-fail  { background:rgba(239,68,68,.15);  color:var(--fail); }
  .state-error      { background:rgba(239,68,68,.15);  color:var(--fail); }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.4} }

  .unmatched-item { padding:8px 18px; font-size:12px; color:var(--warn);
                    display:flex; align-items:center; gap:6px; }

  main { overflow-y:auto; padding:28px; }

  #welcome { display:flex; flex-direction:column; align-items:center;
             justify-content:center; height:100%; gap:16px; text-align:center; }
  #welcome h2 { font-size:22px; font-weight:500; }
  #welcome p  { color:var(--muted); font-size:14px; max-width:480px; line-height:1.6; }
  .folder-box { background:var(--surface); border:1px solid var(--border);
                border-radius:10px; padding:18px 28px; text-align:left;
                font-size:13px; line-height:2.2; min-width:360px; }
  .folder-box b { color:var(--accent); }

  #detail { display:none; }
  .detail-header { display:flex; align-items:flex-start;
                   justify-content:space-between; margin-bottom:24px; gap:16px; }
  .detail-title { font-size:20px; font-weight:600; }
  .detail-meta  { font-size:12px; color:var(--muted); margin-top:4px; }
  .detail-actions { display:flex; align-items:center; gap:10px; flex-shrink:0; }
  .status-pill { font-size:13px; font-weight:700; padding:6px 18px; border-radius:20px; }
  .pill-pass { background:rgba(34,197,94,.15); color:var(--pass); }
  .pill-fail { background:rgba(239,68,68,.15);  color:var(--fail); }
  .pill-err  { background:rgba(245,158,11,.15); color:var(--warn); }
  .dl-btn { background:rgba(99,102,241,.15); color:#a5b4fc;
            border:1px solid rgba(99,102,241,.3); padding:6px 16px; border-radius:6px;
            font-size:13px; font-weight:600; cursor:pointer; text-decoration:none;
            display:inline-flex; align-items:center; gap:6px; transition:background .2s; }
  .dl-btn:hover { background:rgba(99,102,241,.25); }
  .dl-btn.disabled { opacity:.4; cursor:default; pointer-events:none; }

  .state-banner { display:flex; align-items:center; gap:12px; padding:12px 16px;
                  border-radius:8px; margin-bottom:20px; font-size:13px; }
  .state-banner.validating { background:rgba(99,102,241,.12);
                              border:1px solid rgba(99,102,241,.25); color:#a5b4fc; }
  .state-banner.new        { background:rgba(59,130,246,.1);
                              border:1px solid rgba(59,130,246,.25); color:#60a5fa; }
  .state-banner.changed    { background:rgba(245,158,11,.1);
                              border:1px solid rgba(245,158,11,.25); color:var(--warn); }

  .spinner { width:14px; height:14px; border:2px solid currentColor;
             border-top-color:transparent; border-radius:50%;
             animation:spin .7s linear infinite; flex-shrink:0; }
  @keyframes spin { to { transform:rotate(360deg); } }

  .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
           gap:12px; margin-bottom:24px; }
  .card  { background:var(--surface); border:1px solid var(--border);
           border-radius:10px; padding:16px 18px; }
  .card .num { font-size:26px; font-weight:700; }
  .card .lbl { font-size:11px; color:var(--muted); margin-top:4px; }
  .card.warn .num { color:var(--fail); }
  .card.ok   .num { color:var(--pass); }

  .section-title { font-size:13px; font-weight:600; color:var(--muted);
                   text-transform:uppercase; letter-spacing:.06em; margin:24px 0 12px; }

  .tbl-wrap { border:1px solid var(--border); border-radius:10px;
              overflow:hidden; margin-bottom:28px; }
  table { width:100%; border-collapse:collapse; font-size:13px; }
  th { background:var(--surface2); color:var(--muted); font-size:11px;
       font-weight:600; text-transform:uppercase; letter-spacing:.05em;
       padding:10px 14px; text-align:left; }
  td { padding:9px 14px; border-top:1px solid var(--border); }
  tr:hover td { background:var(--surface2); }
  .type-num { color:var(--info);  font-size:11px; font-weight:600; }
  .type-str { color:var(--muted); font-size:11px; }
  .pct-bar-wrap { display:flex; align-items:center; gap:8px; }
  .pct-bar  { height:6px; border-radius:3px; background:var(--border); flex:1; }
  .pct-fill { height:100%; border-radius:3px; background:var(--pass); transition:width .4s; }
  .pct-fill.low { background:var(--fail); }
  .pct-fill.mid { background:var(--warn); }
  .pct-val  { font-size:12px; font-weight:600; min-width:40px; text-align:right; }

  .row-expander { cursor:pointer; }
  .row-expander:hover td { background:rgba(99,102,241,.07); }
  .expand-icon { color:var(--muted); font-size:11px; transition:transform .2s; }
  .expand-icon.open { transform:rotate(90deg); }
  .mismatch-detail    { display:none; }
  .mismatch-detail td { padding:0; }
  .mismatch-inner { padding:12px 14px 16px 32px; }
  .mismatch-inner table { border:1px solid var(--border); border-radius:6px;
                           overflow:hidden; font-size:12px; }
  .mismatch-inner td { background:var(--bg); }
  .diff-old { color:var(--fail); }
  .diff-new { color:var(--pass); }

  .mapping-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:24px; }
  .map-box    { background:var(--surface); border:1px solid var(--border);
                border-radius:8px; padding:14px 16px; }
  .map-box h4 { font-size:11px; font-weight:600; color:var(--muted);
                text-transform:uppercase; letter-spacing:.06em; margin-bottom:10px; }
  .map-tag         { display:inline-block; background:var(--surface2); color:var(--text);
                     font-size:11px; padding:3px 8px; border-radius:4px;
                     margin:2px; border:1px solid var(--border); }
  .map-tag.numeric { border-color:var(--info); color:var(--info); }
  .map-tag.warn    { border-color:var(--warn); color:var(--warn); }

  .error-box { background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.3);
               border-radius:8px; padding:14px 18px; color:var(--fail);
               font-size:13px; margin-bottom:20px; }

  #toast-container { position:fixed; bottom:24px; right:24px;
                     display:flex; flex-direction:column-reverse; gap:8px; z-index:200; }
  .toast { background:var(--surface); border:1px solid var(--border);
           border-radius:8px; padding:12px 18px; font-size:13px; max-width:340px;
           box-shadow:0 4px 16px rgba(0,0,0,.4);
           display:flex; align-items:flex-start; gap:10px;
           animation:slideIn .25s ease; }
  .toast.removing { animation:slideOut .25s ease forwards; }
  .toast-icon { font-size:16px; flex-shrink:0; margin-top:1px; }
  .toast-msg  { flex:1; line-height:1.45; }
  .toast.info    { border-left:3px solid var(--info); }
  .toast.success { border-left:3px solid var(--pass); }
  .toast.warn    { border-left:3px solid var(--warn); }
  .toast.error   { border-left:3px solid var(--fail); }
  @keyframes slideIn  { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:none} }
  @keyframes slideOut { to{opacity:0;transform:translateX(20px)} }

  .modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,.6);
                   display:none; align-items:center; justify-content:center; z-index:100; }
  .modal-overlay.open { display:flex; }
  .modal { background:var(--surface); border:1px solid var(--border);
           border-radius:12px; width:640px; max-height:80vh;
           display:flex; flex-direction:column; overflow:hidden; }
  .modal-head { padding:18px 20px; border-bottom:1px solid var(--border);
                display:flex; align-items:center; justify-content:space-between; }
  .modal-head h3 { font-size:15px; font-weight:600; }
  .modal-close { background:none; border:none; color:var(--muted);
                 font-size:20px; cursor:pointer; }
  .modal-close:hover { color:var(--text); }
  .modal-body { overflow-y:auto; padding:16px 20px; }

  .log-entry { display:flex; align-items:baseline; gap:10px; padding:7px 10px;
               border-radius:6px; font-size:12px; margin-bottom:4px;
               border-left:3px solid transparent; }
  .log-entry.info    { border-color:var(--info);  background:rgba(59,130,246,.05); }
  .log-entry.success { border-color:var(--pass);  background:rgba(34,197,94,.05); }
  .log-entry.warn    { border-color:var(--warn);  background:rgba(245,158,11,.05); }
  .log-entry.error   { border-color:var(--fail);  background:rgba(239,68,68,.05); }
  .log-ts  { color:var(--muted); flex-shrink:0; font-family:monospace; font-size:11px; }
  .log-msg { flex:1; line-height:1.45; }
  .log-icon { flex-shrink:0; }

  .report-row { display:flex; align-items:center; justify-content:space-between;
                padding:10px 12px; border-radius:8px; margin-bottom:6px;
                background:var(--surface2); font-size:13px; gap:12px; }
  .report-name { font-weight:500; flex:1; min-width:0;
                 white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .report-meta { font-size:11px; color:var(--muted); white-space:nowrap; }
  .report-dl { background:rgba(99,102,241,.15); color:#a5b4fc;
               border:1px solid rgba(99,102,241,.3); padding:4px 12px;
               border-radius:5px; font-size:12px; font-weight:600;
               text-decoration:none; }
  .report-dl:hover { background:rgba(99,102,241,.25); }
  .empty-msg { color:var(--muted); font-size:14px; text-align:center; padding:32px; }

  .scanning-dot { width:8px; height:8px; border-radius:50%; background:var(--accent);
                  display:inline-block; animation:pulse 1s ease-in-out infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

  ::-webkit-scrollbar       { width:6px; }
  ::-webkit-scrollbar-track { background:transparent; }
  ::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
</style>
</head>
<body>

<header>
  <div class="logo">&#x2B21; <span>SAP</span> Migration Validator</div>
  <div class="header-right">
    <span id="scan-indicator" style="display:none"><span class="scanning-dot"></span></span>
    <span class="last-scan" id="last-scan-label">Not scanned yet</span>
    <button class="hbtn" id="log-btn"     onclick="openLog()">&#128221; Activity Log</button>
    <button class="hbtn" id="reports-btn" onclick="openReports()">&#128196; Excel Reports</button>
    <button class="hbtn" id="scan-btn"    onclick="triggerScan()">&#8635; Scan Now</button>
  </div>
</header>

<div class="layout">
  <aside>
    <div class="sidebar-head">Tables</div>
    <div id="table-list"></div>
  </aside>
  <main>
    <div id="welcome">
      <h2>Post-Load Validation Dashboard</h2>
      <p>Drop your source and target CSV or XLSX files into the folders below.
         New files are detected within 5 seconds, validated automatically,
         and a toast notification confirms completion.</p>
      <div class="folder-box" id="folder-paths">
        <div>&#128194; Source &#8594; <b>data/source/</b></div>
        <div>&#128194; Target &#8594; <b>data/target/</b></div>
        <div>&#128196; Reports &#8594; <b>reports/</b></div>
        <div style="margin-top:10px;color:#7c82a0;font-size:12px">
          Files matched by name &mdash; MATERIAL.csv &#8596; MATERIAL.csv
        </div>
      </div>
    </div>
    <div id="detail"></div>
  </main>
</div>

<div id="toast-container"></div>

<div class="modal-overlay" id="log-modal">
  <div class="modal">
    <div class="modal-head">
      <h3>&#128221; Activity Log</h3>
      <button class="modal-close" onclick="closeLog()">&times;</button>
    </div>
    <div class="modal-body" id="log-list">
      <div class="empty-msg">No activity yet.</div>
    </div>
  </div>
</div>

<div class="modal-overlay" id="reports-modal">
  <div class="modal">
    <div class="modal-head">
      <h3>&#128196; Excel Reports</h3>
      <button class="modal-close" onclick="closeReports()">&times;</button>
    </div>
    <div class="modal-body" id="reports-list">
      <div class="empty-msg">Loading&hellip;</div>
    </div>
  </div>
</div>

<script>
let activeTable   = null;
let allResults    = {};
let allFileStates = {};
let lastLogCount  = 0;

const ICONS = { info:'&#8505;', success:'&#10003;', warn:'&#9888;', error:'&#10060;' };

function showToast(msg, level) {
  level = level || 'info';
  const el = document.createElement('div');
  el.className = 'toast ' + level;
  el.innerHTML = '<span class="toast-icon">' + (ICONS[level]||'') + '</span>' +
                 '<span class="toast-msg">' + esc(msg) + '</span>';
  document.getElementById('toast-container').appendChild(el);
  setTimeout(function() {
    el.classList.add('removing');
    setTimeout(function() { el.remove(); }, 260);
  }, 5000);
}

async function init() {
  const folders = await fetch('/api/folders').then(r => r.json());
  document.getElementById('folder-paths').innerHTML =
    '<div>&#128194; Source &rarr; <b>' + folders.source_dir + '</b></div>' +
    '<div>&#128194; Target &rarr; <b>' + folders.target_dir + '</b></div>' +
    '<div>&#128196; Reports &rarr; <b>' + folders.reports_dir + '</b></div>' +
    '<div style="margin-top:10px;color:#7c82a0;font-size:12px">Files matched by name</div>';
  await refresh();
  setInterval(refresh, 4000);
}

async function refresh() {
  const [status, results, activity] = await Promise.all([
    fetch('/api/status').then(r => r.json()),
    fetch('/api/results').then(r => r.json()),
    fetch('/api/activity').then(r => r.json()),
  ]);

  document.getElementById('scan-indicator').style.display = status.scanning ? 'inline-block' : 'none';
  document.getElementById('scan-btn').disabled = status.scanning;
  if (status.last_scan)
    document.getElementById('last-scan-label').textContent = 'Last scan: ' + status.last_scan;

  // Show toasts for new log entries
  const newEntries = activity.slice(0, activity.length - lastLogCount);
  if (lastLogCount > 0) newEntries.forEach(function(e) { showToast(e.message, e.level); });
  lastLogCount = activity.length;

  allResults    = {};
  allFileStates = status.file_states || {};
  results.forEach(function(r) { allResults[r.name] = r; });

  renderSidebar(status);

  if (activeTable) {
    const fs = allFileStates[activeTable];
    if (fs && fs.state === 'validating') {
      renderValidatingPlaceholder(activeTable, fs);
    } else if (allResults[activeTable]) {
      renderDetail(allResults[activeTable]);
    }
  }
}

async function triggerScan() {
  await fetch('/api/scan', { method:'POST' });
  setTimeout(refresh, 600);
}

function renderSidebar(status) {
  const list = document.getElementById('table-list');
  let html = '';
  status.pairs.forEach(function(pair) {
    const fs    = (status.file_states || {})[pair.name] || {};
    const state = fs.state || '';

    if (!pair.has_pair) {
      html += '<div class="unmatched-item">&#9888; ' + pair.name +
        ' <span style="font-size:11px;color:#7c82a0">(' +
        (pair.source_path ? 'no target' : 'no source') + ')</span></div>';
      return;
    }

    let pill = '';
    if      (state === 'validating') pill = '<span class="state-pill state-validating">Validating&hellip;</span>';
    else if (state === 'new')        pill = '<span class="state-pill state-new">New</span>';
    else if (state === 'changed')    pill = '<span class="state-pill state-changed">Changed</span>';
    else if (state === 'error')      pill = '<span class="state-pill state-error">Error</span>';
    else {
      const r  = allResults[pair.name];
      const st = r ? r.status : '';
      if      (st === 'PASS')  pill = '<span class="state-pill state-done-pass">PASS</span>';
      else if (st === 'FAIL')  pill = '<span class="state-pill state-done-fail">FAIL</span>';
      else if (st === 'ERROR') pill = '<span class="state-pill state-error">ERROR</span>';
      else                     pill = '<span class="state-pill state-new">&hellip;</span>';
    }

    const act = activeTable === pair.name ? 'active' : '';
    html += '<div class="table-item ' + act + '" onclick="selectTable(\'' + pair.name + '\', this)">' +
            '<span class="tname">' + pair.name + '</span>' + pill + '</div>';
  });

  if (!html) html = '<div style="padding:20px 18px;font-size:13px;color:var(--muted)">No file pairs found.<br>Drop files into source/ and target/.</div>';
  list.innerHTML = html;
}

function selectTable(name, el) {
  activeTable = name;
  document.querySelectorAll('.table-item').forEach(function(e) { e.classList.remove('active'); });
  if (el) el.classList.add('active');

  const fs = allFileStates[name] || {};
  if (fs.state === 'validating') { renderValidatingPlaceholder(name, fs); return; }
  const r = allResults[name];
  if (r) { renderDetail(r); return; }

  document.getElementById('welcome').style.display = 'none';
  document.getElementById('detail').style.display  = 'block';
  document.getElementById('detail').innerHTML =
    '<div class="state-banner new"><span class="spinner"></span>' +
    '<span>&#128194; <b>' + name + '</b> — files detected, waiting for validation&hellip;</span></div>';
}

function renderValidatingPlaceholder(name, fs) {
  document.getElementById('welcome').style.display = 'none';
  document.getElementById('detail').style.display  = 'block';
  document.getElementById('detail').innerHTML =
    '<div class="state-banner validating"><span class="spinner"></span>' +
    '<span><b>' + name + '</b> is being validated now&hellip; ' +
    (fs.source_file ? '(' + fs.source_file + ' &harr; ' + fs.target_file + ')' : '') +
    '</span></div>' +
    '<div style="color:var(--muted);font-size:13px;padding:20px 0">Results will appear here automatically when complete.</div>';
}

function renderDetail(r) {
  document.getElementById('welcome').style.display = 'none';
  const det = document.getElementById('detail');
  det.style.display = 'block';

  const pillCls = r.status==='PASS' ? 'pill-pass' : r.status==='ERROR' ? 'pill-err' : 'pill-fail';
  const fs = allFileStates[r.name] || {};

  let bannerHtml = '';
  if (fs.state === 'changed')
    bannerHtml = '<div class="state-banner changed">&#9888; File changed since last validation — results below may be outdated. Re-validation is queued.</div>';

  const dlBtn = r.excel_file
    ? '<a class="dl-btn" href="/api/download/' + r.name + '" download="' + r.excel_file + '">&#8595; Excel Report</a>'
    : '<span class="dl-btn disabled">&#8595; Excel Report</span>';

  const errHtml = (r.errors && r.errors.length)
    ? '<div class="error-box">&#10060; ' + r.errors.join('<br>') + '</div>' : '';

  const s = r.records_only_in_source, t = r.records_only_in_target;
  const cardsHtml =
    '<div class="cards">' +
    card(fmt(r.total_source_records), 'Source Records', '') +
    card(fmt(r.total_target_records), 'Target Records', '') +
    card(fmt(r.records_matched),      'Keys Matched',   'ok') +
    card(s, 'Source Only', s ? 'warn' : '') +
    card(t, 'Target Only', t ? 'warn' : '') +
    card(r.fields_passed, 'Fields Passed', 'ok') +
    card(r.fields_failed, 'Fields Failed', r.fields_failed ? 'warn' : 'ok') +
    card(r.pass_rate_pct + '%', 'Pass Rate', '') +
    '</div>';

  let mapHtml = '';
  if (r.mapping) {
    const m = r.mapping;
    const srcOnly = m.source_only_fields.length
      ? m.source_only_fields.map(function(f){ return '<span class="map-tag warn">'+f+'</span>'; }).join('')
      : '<span style="color:var(--muted);font-size:12px">none</span>';
    const tgtOnly = m.target_only_fields.length
      ? m.target_only_fields.map(function(f){ return '<span class="map-tag warn">'+f+'</span>'; }).join('')
      : '<span style="color:var(--muted);font-size:12px">none</span>';
    const nums = m.numeric_fields.length
      ? m.numeric_fields.map(function(f){ return '<span class="map-tag numeric">'+f+' &plusmn;'+m.tolerance_map[f]+'</span>'; }).join('')
      : '<span style="color:var(--muted);font-size:12px">none</span>';
    mapHtml =
      '<div class="section-title">Auto-Detected Mapping</div>' +
      '<div class="mapping-grid">' +
      '<div class="map-box"><h4>Join key</h4><span class="map-tag">' + m.join_key + '</span></div>' +
      '<div class="map-box"><h4>Numeric fields (auto-tolerance)</h4>' + nums + '</div>' +
      '<div class="map-box"><h4>Source-only columns (skipped)</h4>' + srcOnly + '</div>' +
      '<div class="map-box"><h4>Target-only columns (skipped)</h4>' + tgtOnly + '</div>' +
      '</div>';
  }

  const fieldRows = r.field_results.map(function(fr, i) {
    const pct     = fr.match_pct;
    const fillCls = pct >= 95 ? '' : pct >= 80 ? 'mid' : 'low';
    const stBadge = fr.status === 'PASS'
      ? '<span style="background:rgba(34,197,94,.15);color:var(--pass);font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px">PASS</span>'
      : '<span style="background:rgba(239,68,68,.15);color:var(--fail);font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px">FAIL</span>';
    const typeTag = fr.type === 'numeric'
      ? '<span class="type-num">numeric<br><small>&plusmn;' + fr.tolerance + '</small></span>'
      : '<span class="type-str">string</span>';
    const hasMiss = fr.mismatches && fr.mismatches.length > 0;
    const expIcon = hasMiss ? '<span class="expand-icon" id="ei-' + i + '">&blacktriangleright;</span> ' : '';

    const missRows = hasMiss ? fr.mismatches.slice(0,20).map(function(m) {
      return '<tr><td>' + m.material + '</td>' +
             '<td class="diff-old">' + esc(String(m.source_value)) + '</td>' +
             '<td class="diff-new">' + esc(String(m.target_value)) + '</td>' +
             '<td style="color:var(--muted)">' + esc(m.issue) + '</td></tr>';
    }).join('') : '';

    const detailRow = hasMiss
      ? '<tr class="mismatch-detail" id="md-' + i + '">' +
        '<td colspan="7"><div class="mismatch-inner"><table>' +
        '<thead><tr><th>Key</th><th>Source Value</th><th>Target Value</th><th>Issue</th></tr></thead>' +
        '<tbody>' + missRows + '</tbody></table></div></td></tr>'
      : '';

    return '<tr class="' + (hasMiss ? 'row-expander' : '') + '"' +
           (hasMiss ? ' onclick="toggleRow(' + i + ')"' : '') + '>' +
           '<td>' + expIcon + fr.field + '</td>' +
           '<td>' + typeTag + '</td>' +
           '<td>' + fr.total + '</td>' +
           '<td>' + fr.matched + '</td>' +
           '<td>' + (fr.mismatched + fr.miss_source + fr.miss_target) + '</td>' +
           '<td><div class="pct-bar-wrap"><div class="pct-bar">' +
           '<div class="pct-fill ' + fillCls + '" style="width:' + pct + '%"></div>' +
           '</div><span class="pct-val">' + pct + '%</span></div></td>' +
           '<td>' + stBadge + '</td></tr>' + detailRow;
  }).join('');

  det.innerHTML =
    bannerHtml +
    '<div class="detail-header">' +
    '<div><div class="detail-title">' + r.name + '</div>' +
    '<div class="detail-meta">' + r.source_file + ' &harr; ' + r.target_file +
    ' &nbsp;&middot;&nbsp; Validated: ' + r.run_at + '</div></div>' +
    '<div class="detail-actions">' + dlBtn +
    '<span class="status-pill ' + pillCls + '">' + r.status + '</span></div></div>' +
    errHtml + cardsHtml + mapHtml +
    '<div class="section-title">Field-Level Results</div>' +
    '<div class="tbl-wrap"><table><thead><tr>' +
    '<th>Field</th><th>Type</th><th>Total</th><th>Matched</th>' +
    '<th>Issues</th><th>Match %</th><th>Status</th>' +
    '</tr></thead><tbody>' + fieldRows + '</tbody></table></div>';
}

async function openLog() {
  document.getElementById('log-modal').classList.add('open');
  const activity = await fetch('/api/activity').then(r => r.json());
  const el = document.getElementById('log-list');
  if (!activity.length) { el.innerHTML = '<div class="empty-msg">No activity yet.</div>'; return; }
  const LI = { info:'&#8505;', success:'&#10003;', warn:'&#9888;', error:'&#10060;' };
  el.innerHTML = activity.map(function(e) {
    return '<div class="log-entry ' + e.level + '">' +
           '<span class="log-ts">' + e.ts + '</span>' +
           '<span class="log-icon">' + (LI[e.level]||'') + '</span>' +
           '<span class="log-msg">' + esc(e.message) + '</span></div>';
  }).join('');
}
function closeLog() { document.getElementById('log-modal').classList.remove('open'); }

async function openReports() {
  document.getElementById('reports-modal').classList.add('open');
  const list = document.getElementById('reports-list');
  list.innerHTML = '<div class="empty-msg">Loading&hellip;</div>';
  const reports = await fetch('/api/reports').then(r => r.json());
  if (!reports.length) {
    list.innerHTML = '<div class="empty-msg">No Excel reports yet.<br>Run a scan to generate them.</div>';
    return;
  }
  list.innerHTML = reports.map(function(rep) {
    return '<div class="report-row">' +
           '<span class="report-name">&#128196; ' + rep.filename + '</span>' +
           '<span class="report-meta">' + rep.size_kb + ' KB &nbsp; ' + rep.modified + '</span>' +
           '<a class="report-dl" href="/api/download-file/' + encodeURIComponent(rep.filename) +
           '" download="' + rep.filename + '">&#8595; Download</a></div>';
  }).join('');
}
function closeReports() { document.getElementById('reports-modal').classList.remove('open'); }

['log-modal','reports-modal'].forEach(function(id) {
  document.getElementById(id).addEventListener('click', function(e) {
    if (e.target === this) this.classList.remove('open');
  });
});

function toggleRow(i) {
  const row  = document.getElementById('md-' + i);
  const icon = document.getElementById('ei-' + i);
  const open = row.style.display === 'table-row';
  row.style.display = open ? 'none' : 'table-row';
  icon.classList.toggle('open', !open);
}
function card(val, lbl, cls) {
  return '<div class="card ' + cls + '"><div class="num">' + val +
         '</div><div class="lbl">' + lbl + '</div></div>';
}
function fmt(n) { return Number(n).toLocaleString(); }
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

init();
</script>
</body>
</html>

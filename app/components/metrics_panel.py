from pathlib import Path

import streamlit as st


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

:root {
  --background: #f8f9ff;
  --surface: #ffffff;
  --surface-low: #eff4ff;
  --surface-container: #e5eeff;
  --text: #0b1c30;
  --muted: #64748b;
  --outline: #e2e8f0;
  --primary: #006c49;
  --primary-bright: #10b981;
  --secondary: #006591;
  --secondary-bright: #39b8fd;
  --tertiary: #b91a24;
  --danger: #ef4444;
  --slate: #1e293b;
}

html, body, [class*="css"] { font-family: "Inter", sans-serif; }
.stApp { background: var(--background); color: var(--text); }
[data-testid="stSidebar"] {
  background: #f8fafc;
  border-right: 1px solid var(--outline);
  min-width: 260px;
}
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { margin: 0; }
[data-testid="stSidebar"] a {
  min-height: 42px;
  border-radius: 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
}
[data-testid="stSidebar"] a:hover {
  background: #f1f5f9;
  color: #006c49;
}
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; }
.material-symbols-outlined {
  font-family: "Material Symbols Outlined";
  font-weight: normal;
  font-style: normal;
  font-size: 22px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-feature-settings: "liga";
  -webkit-font-smoothing: antialiased;
}

.gv-side-brand {
  padding: 18px 18px 22px;
  border-bottom: 1px solid var(--outline);
  margin-bottom: 14px;
}
.gv-side-title { color: var(--primary-bright); font-size: 18px; font-weight: 900; }
.gv-side-subtitle { color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: .18em; text-transform: uppercase; margin-top: 2px; }
.gv-active-nav {
  min-height: 48px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  background: #ffffff;
  color: var(--primary);
  border-left-color: var(--primary-bright);
  border-left: 4px solid var(--primary-bright);
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
  margin: 4px -8px 4px -8px;
}
.gv-sidebar-footer {
  border-top: 1px solid var(--outline);
  margin-top: 24px;
  padding-top: 14px;
  display: grid;
  gap: 4px;
}
.gv-sidebar-footer a {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #64748b;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.gv-sidebar-footer a:hover { background: #f1f5f9; color: var(--primary); text-decoration: none; }

.gv-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 16px 0 22px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 28px;
}

.gv-brand { display: flex; align-items: center; gap: 12px; }
.gv-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: var(--slate);
  color: white;
  display: grid;
  place-items: center;
  font-weight: 800;
}
.gv-title { font-size: 22px; font-weight: 800; letter-spacing: 0; margin: 0; }
.gv-subtitle { color: #64748b; font-size: 13px; margin-top: 1px; }
.gv-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 999px;
  border: 1px solid rgba(16, 185, 129, .25);
  background: rgba(16, 185, 129, .08);
  color: var(--primary);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}
.gv-dot { width: 8px; height: 8px; border-radius: 999px; background: var(--primary-bright); }

.page-kicker {
  color: var(--primary);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .05em;
  margin-bottom: 8px;
}
.page-title { font-size: 32px; line-height: 1.2; font-weight: 800; margin: 0; }
.page-copy { color: #64748b; font-size: 16px; line-height: 1.6; margin-top: 8px; max-width: 820px; }
.gv-card { background: var(--surface); border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; }
.gv-card-title { font-size: 20px; font-weight: 800; margin: 0 0 6px; }
.gv-card-copy { color: var(--muted); font-size: 14px; line-height: 1.5; margin: 0; }

.upload-tile {
  position: relative;
  min-height: 400px;
  background:
    radial-gradient(#006c49 1px, transparent 1px) 0 0 / 20px 20px,
    #ffffff;
  border: 1px solid #bbcabf;
  border-radius: 8px;
  padding: 24px;
  display: grid;
  place-items: center;
  text-align: center;
  overflow: hidden;
}
.upload-tile::before {
  content: "";
  position: absolute;
  inset: 0;
  background: #ffffff;
  opacity: .92;
}
.upload-tile:hover { border-color: var(--primary); }
.upload-tile-inner { position: relative; z-index: 1; max-width: 360px; }
.upload-icon {
  width: 66px;
  height: 66px;
  border-radius: 999px;
  background: var(--surface-container);
  color: var(--primary);
  display: grid;
  place-items: center;
  margin: 0 auto 22px;
}
.upload-title { font-size: 20px; font-weight: 800; margin-bottom: 8px; }
.upload-copy { color: #64748b; font-size: 14px; margin-bottom: 18px; }
.upload-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: 8px;
  color: white;
  background: #1e293b;
  font-size: 13px;
  font-weight: 800;
}

.metric-card {
  background: var(--surface);
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px 22px;
  min-height: 144px;
}
.metric-label { color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; }
.metric-value { font-size: 32px; line-height: 1.2; font-weight: 800; color: var(--text); margin-top: 18px; }
.metric-note { margin-top: 8px; color: #64748b; font-size: 13px; }
.chip-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
.chip {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: .03em;
  text-transform: uppercase;
}
.chip-new { background: rgba(16, 185, 129, .1); color: #006c49; }
.chip-removed { background: rgba(239, 68, 68, .1); color: #b91a24; }
.chip-unchanged { background: rgba(14, 165, 233, .12); color: #006591; }

.bar-wrap { display: grid; grid-template-columns: repeat(4, minmax(110px, 1fr)); gap: 28px; align-items: end; min-height: 270px; }
.bar-group { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; height: 210px; align-items: end; }
.bar { border-radius: 6px 6px 0 0; min-height: 14px; }
.bar-label { color: #64748b; font-size: 12px; font-weight: 700; text-align: center; text-transform: uppercase; letter-spacing: .05em; margin-top: 12px; }
.insight { background: #f8fafc; border-left: 4px solid var(--primary-bright); border-radius: 8px; padding: 15px 16px; margin-bottom: 14px; }
.insight strong { display: block; color: var(--primary); font-size: 12px; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 6px; }
.pipeline-step { display: flex; gap: 16px; padding: 18px 0; border-bottom: 1px solid #e2e8f0; }
.pipeline-index {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: grid;
  place-items: center;
  color: white;
  background: var(--slate);
  font-weight: 800;
  flex: 0 0 auto;
}
.stButton>button { border-radius: 8px; border: 1px solid var(--primary); background: var(--primary); color: white; font-weight: 700; }
.stDownloadButton>button { border-radius: 8px; font-weight: 700; }
[data-testid="stFileUploader"] {
  margin-top: 18px;
}
[data-testid="stFileUploader"] > div:last-child:not(:has(section)) {
  display: none;
}
[data-testid="stFileUploaderDropzone"] {
  border: 1px dashed #94a3b8;
  border-radius: 8px;
  background: rgba(248, 250, 252, .92);
  min-height: 96px;
  padding: 28px;
}
[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--primary);
}

.result-frame {
  background: #ffffff;
  border: 1px solid var(--outline);
  border-radius: 8px;
  overflow: hidden;
}
.result-frame-head {
  padding: 18px 22px;
  border-bottom: 1px solid var(--outline);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}
.result-stage {
  position: relative;
  height: 360px;
  background: #0f172a;
  overflow: hidden;
}
.result-stage img {
  width: 100%;
  height: 360px;
  object-fit: contain;
  display: block;
  background: #0f172a;
}
.map-controls {
  position: absolute;
  top: 24px;
  right: 24px;
  background: rgba(255,255,255,.92);
  border: 1px solid rgba(226,232,240,.9);
  border-radius: 8px;
  box-shadow: 0 12px 28px rgba(15,23,42,.12);
  display: grid;
  overflow: hidden;
}
.map-control {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  color: #334155;
  border-bottom: 1px solid #e2e8f0;
}
.map-control:last-child { border-bottom: 0; }
.map-hud {
  position: absolute;
  left: 24px;
  bottom: 24px;
  display: flex;
  gap: 18px;
  background: rgba(15,23,42,.86);
  color: white;
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 8px;
  padding: 14px 16px;
  backdrop-filter: blur(8px);
}
.hud-label {
  color: #94a3b8;
  display: block;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.hud-value {
  display: block;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 20px;
  font-weight: 700;
  margin-top: 4px;
}
.heatmap-legend {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #64748b;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.heatmap-scale {
  width: 190px;
  height: 12px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(16,185,129,.25), rgba(245,158,11,.7), rgba(239,68,68,.95));
}
.compact-image {
  border: 1px solid var(--outline);
  border-radius: 8px;
  background: #0f172a;
  overflow: hidden;
  height: 300px;
  display: grid;
  place-items: center;
}
.compact-image img {
  width: 100%;
  height: 300px;
  object-fit: contain;
  display: block;
}
.empty-results {
  background: #ffffff;
  border: 1px dashed #94a3b8;
  border-radius: 8px;
  padding: 48px 28px;
  text-align: center;
  color: #64748b;
}
.empty-results .material-symbols-outlined {
  color: var(--primary);
  font-size: 44px;
  margin-bottom: 12px;
}

@media (max-width: 900px) {
  .gv-topbar { align-items: flex-start; flex-direction: column; }
  .bar-wrap { grid-template-columns: repeat(2, minmax(110px, 1fr)); }
}
</style>
"""


def inject_styles():
    st.markdown(CSS, unsafe_allow_html=True)


def topbar(metrics):
    status = "System Ready" if metrics else "Awaiting Analysis"
    st.markdown(
        f"""
        <div class="gv-topbar">
          <div class="gv-brand">
            <div class="gv-logo">GV</div>
            <div>
              <p class="gv-title">GeoVision</p>
              <div class="gv-subtitle">Satellite Change Analytics</div>
            </div>
          </div>
          <div class="gv-status"><span class="gv-dot"></span>{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_nav(active):
    items = [
        ("Home", ":material/home:", "main.py", "home"),
        ("Upload", ":material/cloud_upload:", "pages/1_Upload.py", "cloud_upload"),
        ("Results", ":material/visibility:", "pages/2_Results.py", "visibility"),
        ("Analytics", ":material/analytics:", "pages/3_Analytics.py", "analytics"),
        ("About", ":material/info:", "pages/4_About.py", "info"),
    ]
    st.sidebar.markdown(
        """
        <div class="gv-side-brand">
          <div class="gv-side-title">GeoVision</div>
          <div class="gv-side-subtitle">Intelligence Suite</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for label, icon, page, material_icon in items:
        if label == active:
            st.sidebar.markdown(
                f"""
                <div class="gv-active-nav">
                  <span class="material-symbols-outlined">{material_icon}</span>
                  <span>{label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.sidebar.page_link(page, label=label, icon=icon)
    st.sidebar.markdown(
        """
        <div class="gv-sidebar-footer">
          <a href="#"><span class="material-symbols-outlined">settings</span><span>Settings</span></a>
          <a href="#"><span class="material-symbols-outlined">help</span><span>Help</span></a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker, title, copy):
    st.markdown(
        f"""
        <div class="page-kicker">{kicker}</div>
        <h1 class="page-title">{title}</h1>
        <p class="page-copy">{copy}</p>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, note, chip_class="chip-unchanged", chip_text=None):
    chip = f'<span class="chip {chip_class}">{chip_text}</span>' if chip_text else ""
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-note">{note}</div>
          <div class="chip-row">{chip}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metrics_or_default(metrics):
    return metrics or {
        "new": 0,
        "removed": 0,
        "unchanged": 0,
        "total": 0,
        "changed": 0,
        "change_percent": 0,
        "confidence": 0,
        "iou_threshold": 0,
        "paths": {},
    }


def report_bytes(metrics):
    metrics = metrics_or_default(metrics)
    lines = [
        "GeoVision Satellite Change Analytics Report",
        "",
        f"New detections: {metrics['new']}",
        f"Removed detections: {metrics['removed']}",
        f"Unchanged detections: {metrics['unchanged']}",
        f"Total detections: {metrics['total']}",
        f"Change percentage: {metrics['change_percent']:.2f}%",
        f"Confidence threshold: {metrics['confidence']:.2f}",
        f"IoU threshold: {metrics['iou_threshold']:.2f}",
    ]
    if metrics.get("paths"):
        lines.extend(["", "Generated outputs:"])
        lines.extend(str(value) for value in metrics["paths"].values())
    return "\n".join(lines).encode("utf-8")


def project_root():
    return Path(__file__).resolve().parents[2]

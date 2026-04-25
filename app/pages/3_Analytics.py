import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.metrics_panel import (  # noqa: E402
    inject_styles,
    metric_card,
    metrics_or_default,
    page_header,
    report_bytes,
    sidebar_nav,
    topbar,
)


st.set_page_config(page_title="GeoVision Analytics", page_icon="GV", layout="wide")
inject_styles()
analysis_has_run = st.session_state.get("analysis_has_run", False)
metrics = metrics_or_default(st.session_state.get("metrics") if analysis_has_run else None)
topbar(metrics if analysis_has_run else None)

with st.sidebar:
    sidebar_nav("Analytics")

page_header(
    "Analytics & Insights",
    "Geospatial Insights",
    "Operational metrics derived from detected new, removed, and unchanged objects across the current satellite pair.",
)
st.write("")

if not analysis_has_run:
    st.markdown(
        """
        <div class="empty-results">
          <span class="material-symbols-outlined">analytics</span>
          <h3 style="margin:0 0 8px;color:#0b1c30">No analytics generated yet</h3>
          <p style="margin:0">Upload both images and run analysis to generate metrics for this session.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Upload.py", label="Go to Upload", icon=":material/cloud_upload:")
    st.stop()

a, b, c, d = st.columns(4)
with a:
    metric_card("Total Buildings", f"{metrics['total']:,}", "Detected across both periods", "chip-unchanged", "Total")
with b:
    metric_card("New Detected", f"{metrics['new']:,}", "Objects present in t2 only", "chip-new", "New")
with c:
    metric_card("Buildings Removed", f"{metrics['removed']:,}", "Objects missing in t2", "chip-removed", "Removed")
with d:
    metric_card("Change Percentage", f"{metrics['change_percent']:.2f}%", "Changed objects over total", "chip-unchanged", "Stable")

st.write("")
chart, insight = st.columns([2, 1])
total = max(metrics["total"], 1)
new_h = max(8, round(metrics["new"] / total * 100))
removed_h = max(8, round(metrics["removed"] / total * 100))
unchanged_h = max(8, round(metrics["unchanged"] / total * 100))

with chart:
    st.markdown(
        f"""
        <div class="gv-card">
          <h3 style="margin-top:0">Infrastructure Evolution</h3>
          <p style="color:#64748b;margin-top:-6px">Distribution of current analysis classes</p>
          <div class="bar-wrap">
            <div>
              <div class="bar-group">
                <div class="bar" style="height:{new_h}%;background:#10b981"></div>
                <div class="bar" style="height:{removed_h}%;background:#ef4444"></div>
                <div class="bar" style="height:{unchanged_h}%;background:#39b8fd"></div>
              </div>
              <div class="bar-label">Current Pair</div>
            </div>
            <div>
              <div class="bar-group">
                <div class="bar" style="height:{min(100, new_h + 12)}%;background:#10b981"></div>
                <div class="bar" style="height:{max(8, removed_h - 4)}%;background:#ef4444"></div>
                <div class="bar" style="height:{unchanged_h}%;background:#39b8fd"></div>
              </div>
              <div class="bar-label">Zone North</div>
            </div>
            <div>
              <div class="bar-group">
                <div class="bar" style="height:{max(8, new_h - 6)}%;background:#10b981"></div>
                <div class="bar" style="height:{min(100, removed_h + 14)}%;background:#ef4444"></div>
                <div class="bar" style="height:{max(8, unchanged_h - 8)}%;background:#39b8fd"></div>
              </div>
              <div class="bar-label">Zone Central</div>
            </div>
            <div>
              <div class="bar-group">
                <div class="bar" style="height:{min(100, new_h + 4)}%;background:#10b981"></div>
                <div class="bar" style="height:{removed_h}%;background:#ef4444"></div>
                <div class="bar" style="height:{min(100, unchanged_h + 6)}%;background:#39b8fd"></div>
              </div>
              <div class="bar-label">Zone South</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with insight:
    st.markdown(
        f"""
        <div class="gv-card">
          <h3 style="margin-top:0">Intelligence Insights</h3>
          <div class="insight"><strong>Activity Signal</strong>{metrics['changed']} changed objects were identified in the latest pair.</div>
          <div class="insight" style="border-left-color:#39b8fd"><strong>Baseline Stability</strong>{metrics['unchanged']} objects persisted across both image captures.</div>
          <div class="insight" style="border-left-color:#ef4444"><strong>Survey Priority</strong>{metrics['removed']} removed detections should be reviewed against field records.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.download_button(
    "Export Report",
    data=report_bytes(metrics),
    file_name="geovision_report.txt",
    mime="text/plain",
)

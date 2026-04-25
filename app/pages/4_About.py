import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.metrics_panel import inject_styles, page_header, sidebar_nav, topbar  # noqa: E402


st.set_page_config(page_title="GeoVision Methodology", page_icon="GV", layout="wide")
inject_styles()
topbar(st.session_state.get("metrics"))

with st.sidebar:
    sidebar_nav("About")

page_header(
    "System Architecture",
    "Methodology & Processing Pipeline",
    "GeoVision transforms raw satellite imagery into detection layers, temporal change categories, heatmaps, and dashboard-ready metrics.",
)
st.write("")

left, right = st.columns([2, 1])
with left:
    st.markdown(
        """
        <div class="gv-card">
          <div class="pipeline-step">
            <div class="pipeline-index">1</div>
            <div><strong>Input Alignment</strong><br><span style="color:#64748b">The comparison image is resized to the baseline dimensions for pixel-consistent processing.</span></div>
          </div>
          <div class="pipeline-step">
            <div class="pipeline-index">2</div>
            <div><strong>YOLO Detection</strong><br><span style="color:#64748b">The building detector extracts object bounding boxes from both temporal images.</span></div>
          </div>
          <div class="pipeline-step">
            <div class="pipeline-index">3</div>
            <div><strong>Temporal Fusion</strong><br><span style="color:#64748b">IoU, centroid distance, and neighbor similarity classify new, removed, and unchanged features.</span></div>
          </div>
          <div class="pipeline-step" style="border-bottom:0">
            <div class="pipeline-index">4</div>
            <div><strong>Reporting Outputs</strong><br><span style="color:#64748b">Detection images, fusion overlays, heatmaps, and metrics JSON are written to the outputs folder.</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="gv-card" style="background:#1e293b;color:white">
          <h3 style="margin-top:0;color:white">Technical Stack</h3>
          <p><strong>Core Logic</strong><br><span style="color:#cbd5e1">Python / OpenCV</span></p>
          <p><strong>Detection</strong><br><span style="color:#cbd5e1">Ultralytics YOLO</span></p>
          <p><strong>Interface</strong><br><span style="color:#cbd5e1">Streamlit Dashboard</span></p>
          <p><strong>Shared Entry Points</strong><br><span style="color:#cbd5e1">run.py and app/main.py</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

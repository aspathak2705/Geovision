import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.heatmap_view import display_heatmap  # noqa: E402
from app.components.image_viewer import display_fusion_stage, display_image_card, existing_image  # noqa: E402
from app.components.metrics_panel import inject_styles, page_header, sidebar_nav, topbar  # noqa: E402


st.set_page_config(page_title="GeoVision Results", page_icon="GV", layout="wide")
inject_styles()
metrics = st.session_state.get("metrics")
topbar(metrics)

with st.sidebar:
    sidebar_nav("Results")

page_header(
    "Detection & Fusion Results",
    "Temporal Fusion Output",
    "Comparative detection views, semantic change overlays, and change-density heatmap layers generated from project imagery.",
)
st.write("")

analysis_has_run = st.session_state.get("analysis_has_run", False)

if not analysis_has_run:
    st.markdown(
        """
        <div class="empty-results">
          <span class="material-symbols-outlined">query_stats</span>
          <h3 style="margin:0 0 8px;color:#0b1c30">No analysis run in this session</h3>
          <p style="margin:0">Upload images and click Run Analysis to generate detection, fusion, and heatmap outputs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Upload.py", label="Go to Upload", icon=":material/cloud_upload:")
    st.stop()

paths = metrics.get("paths", {}) if metrics else {}
t1_path = existing_image(paths.get("detect_t1", "outputs/detect_t1.jpg"))
t2_path = existing_image(paths.get("detect_t2", "outputs/detect_t2.jpg"))
fusion_path = existing_image(paths.get("fusion", "outputs/fusion.jpg"))

c1, c2 = st.columns(2)
with c1:
    display_image_card("t1 Detection Cluster", t1_path, "Baseline detection layer")
with c2:
    display_image_card("t2 Detection Cluster", t2_path, "Comparison detection layer")

st.write("")
display_fusion_stage("Temporal Fusion Output", fusion_path, metrics or {})

st.write("")
display_heatmap(metrics)

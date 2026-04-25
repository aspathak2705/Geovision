import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.metrics_panel import inject_styles, page_header, sidebar_nav, topbar  # noqa: E402
from app.components.uploader import image_uploader, save_upload  # noqa: E402
from core.pipeline import DEFAULT_T1_PATH, DEFAULT_T2_PATH, run_analysis  # noqa: E402


st.set_page_config(page_title="GeoVision Upload", page_icon="GV", layout="wide")
inject_styles()
metrics = st.session_state.get("metrics")
topbar(metrics)

with st.sidebar:
    sidebar_nav("Upload")

page_header(
    "Upload & Input",
    "Satellite Change Analysis",
    "Upload baseline and comparison imagery, tune detection parameters, and execute the shared GeoVision pipeline.",
)
st.write("")

left, right = st.columns(2)
with left:
    st.markdown(
        """
        <div class="upload-tile-inner">
          <div class="upload-icon"><span class="material-symbols-outlined">satellite_alt</span></div>
          <div class="upload-title">Satellite Image t1</div>
          <div class="upload-copy">Baseline imagery (GeoTIFF, PNG, JPEG)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    t1_upload = image_uploader("Satellite Image t1", "Baseline imagery", "t1_upload")

with right:
    st.markdown(
        """
        <div class="upload-tile-inner">
          <div class="upload-icon"><span class="material-symbols-outlined">history</span></div>
          <div class="upload-title">Satellite Image t2</div>
          <div class="upload-copy">Comparison imagery (GeoTIFF, PNG, JPEG)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    t2_upload = image_uploader("Satellite Image t2", "Comparison imagery", "t2_upload")

st.write("")
controls, action = st.columns([2, 1])
with controls:
    st.markdown('<div class="gv-card">', unsafe_allow_html=True)
    st.subheader("Analysis Configuration")
    confidence = st.slider("Confidence threshold", 0.10, 0.95, 0.60, 0.05)
    iou_threshold = st.slider("Matching sensitivity", 0.10, 0.80, 0.30, 0.05)
    st.caption("Higher confidence reduces low-probability detections. Higher matching sensitivity requires tighter temporal alignment.")
    st.markdown("</div>", unsafe_allow_html=True)

with action:
    st.markdown('<div class="gv-card">', unsafe_allow_html=True)
    st.subheader("Ready to Process")
    st.caption("Runs YOLO detection, temporal fusion, heatmap generation, and metrics export.")
    run_clicked = st.button("Run Analysis", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if run_clicked:
    if t1_upload is None or t2_upload is None:
        st.error("Please upload both t1 and t2 satellite images before running analysis.")
        st.session_state["analysis_has_run"] = False
        st.session_state.pop("metrics", None)
    else:
        save_upload(t1_upload, DEFAULT_T1_PATH)
        save_upload(t2_upload, DEFAULT_T2_PATH)

        with st.spinner("Running GeoVision analysis..."):
            try:
                metrics = run_analysis(
                    DEFAULT_T1_PATH,
                    DEFAULT_T2_PATH,
                    confidence=confidence,
                    iou_threshold=iou_threshold,
                )
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                st.session_state["analysis_has_run"] = False
                st.session_state.pop("metrics", None)
            else:
                st.session_state["metrics"] = metrics
                st.session_state["analysis_has_run"] = True
                st.success("Analysis completed. Results and analytics pages are updated.")

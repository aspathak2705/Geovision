import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.components.metrics_panel import inject_styles, page_header, sidebar_nav, topbar  # noqa: E402


st.set_page_config(
    page_title="GeoVision Dashboard",
    page_icon="GV",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    inject_styles()
    metrics = st.session_state.get("metrics")
    topbar(metrics)

    with st.sidebar:
        sidebar_nav("Home")
        st.divider()
        if st.session_state.get("analysis_has_run"):
            st.success("Current session analysis ready")
        else:
            st.info("Upload images and run analysis")

    page_header(
        "Dashboard Structure",
        "GeoVision Intelligence Suite",
        "Use the sidebar pages to upload imagery, run detection, inspect fusion outputs, review analytics, and read the project methodology.",
    )

    a, b, c, d = st.columns(4)
    for column, title, copy, icon in [
        (a, "Upload Input", "Prepare temporal satellite images for analysis.", "cloud_upload"),
        (b, "Results Visualization", "Inspect detection, fusion, and heatmap outputs.", "visibility"),
        (c, "Analytics Insights", "Review metrics and derived intelligence signals.", "analytics"),
        (d, "System Methodology", "Understand the processing pipeline.", "info"),
    ]:
        column.markdown(
            f"""
            <div class="metric-card">
              <span class="material-symbols-outlined" style="color:#006c49">{icon}</span>
              <div class="metric-value" style="font-size:20px">{title}</div>
              <div class="metric-note">{copy}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()

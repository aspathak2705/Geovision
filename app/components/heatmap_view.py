import streamlit as st

from app.components.image_viewer import display_image_card, existing_image


def display_heatmap(metrics):
    paths = metrics.get("paths", {}) if metrics else {}
    heatmap_path = existing_image(paths.get("heatmap", "outputs/heatmap.jpg"))
    st.markdown(
        """
        <div class="result-frame-head" style="border:1px solid #e2e8f0;border-bottom:0;border-radius:8px 8px 0 0;background:white">
          <div>
            <div class="gv-card-title">Change Density Heatmap</div>
            <p class="gv-card-copy">Density layer for new and removed detections.</p>
          </div>
          <div class="heatmap-legend">
            <span>Low</span>
            <span class="heatmap-scale"></span>
            <span>High</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    display_image_card("Change Density Heatmap", heatmap_path)

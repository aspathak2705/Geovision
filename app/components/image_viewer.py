from pathlib import Path
import base64
import mimetypes

import streamlit as st

from app.components.metrics_panel import project_root


def project_path(relative_path):
    return project_root() / relative_path


def existing_image(relative_path):
    path = project_path(relative_path)
    return path if path.exists() else None


def display_image_card(title, path, caption=None):
    st.markdown(f"**{title}**")
    if path and Path(path).exists():
        uri = image_data_uri(path)
        caption_html = f'<div class="metric-note">{caption}</div>' if caption else ""
        st.markdown(
            f"""
            <div class="compact-image">
              <img src="{uri}" alt="{title}" />
            </div>
            {caption_html}
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("This image will appear after analysis runs.")


def image_data_uri(path):
    path = Path(path)
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def display_fusion_stage(title, path, metrics):
    st.markdown('<div class="result-frame">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="result-frame-head">
          <div>
            <div class="gv-card-title">{title}</div>
            <p class="gv-card-copy">Pixel-level alignment and semantic change analysis.</p>
          </div>
          <div class="chip-row" style="margin-top:0">
            <span class="chip chip-new">New</span>
            <span class="chip chip-removed">Removed</span>
            <span class="chip chip-unchanged">Unchanged</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if path and Path(path).exists():
        uri = image_data_uri(path)
        confidence = metrics.get("confidence", 0) * 100 if metrics else 0
        changed = metrics.get("changed", 0) if metrics else 0
        st.markdown(
            f"""
            <div class="result-stage">
              <img src="{uri}" alt="{title}" />
              <div class="map-controls">
                <div class="map-control"><span class="material-symbols-outlined">add</span></div>
                <div class="map-control"><span class="material-symbols-outlined">remove</span></div>
                <div class="map-control"><span class="material-symbols-outlined">layers</span></div>
              </div>
              <div class="map-hud">
                <div><span class="hud-label">Confidence</span><span class="hud-value">{confidence:.0f}%</span></div>
                <div><span class="hud-label">Changed Objects</span><span class="hud-value">{changed}</span></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Fusion output will appear after analysis runs.")
    st.markdown("</div>", unsafe_allow_html=True)

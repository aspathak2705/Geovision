from pathlib import Path

import streamlit as st


def save_upload(uploaded_file, target_path):
    target_path = Path(target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("wb") as f:
        f.write(uploaded_file.getbuffer())


def image_uploader(label, help_text, key):
    return st.file_uploader(
        f"Select {label.lower()}",
        type=["png", "jpg", "jpeg", "tif", "tiff"],
        key=key,
        label_visibility="collapsed",
    )

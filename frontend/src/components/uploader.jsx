import React from "react";

export function UploadTile({ icon: Icon, title, copy, file, onChange }) {
  return (
    <label className="upload-tile">
      <span className="upload-inner">
        <span className="upload-icon"><Icon size={28} /></span>
        <strong>{title}</strong>
        <span>{copy}</span>
        <span className="upload-pill">{file ? file.name : "Choose image"}</span>
      </span>
      <input
        accept=".png,.jpg,.jpeg,.tif,.tiff"
        onChange={(event) => onChange(event.target.files?.[0] || null)}
        type="file"
      />
    </label>
  );
}

export function Slider({ label, min, max, step, value, onChange }) {
  return (
    <label className="slider-row">
      <span>{label}</span>
      <strong>{value.toFixed(2)}</strong>
      <input min={min} max={max} step={step} value={value} onChange={(event) => onChange(Number(event.target.value))} type="range" />
    </label>
  );
}

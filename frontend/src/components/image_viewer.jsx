import React from "react";
import { Layers, Minus, Plus } from "lucide-react";
import { apiUrl } from "../services/api.js";

export function ImageCard({ title, src, caption }) {
  return (
    <section className="image-card">
      <h3>{title}</h3>
      {src ? <img src={src} alt={title} /> : <div className="image-placeholder">This image will appear after analysis runs.</div>}
      {caption ? <p>{caption}</p> : null}
    </section>
  );
}

export function FusionStage({ metrics }) {
  return (
    <section className="result-frame">
      <div className="frame-head">
        <div>
          <h2>Temporal Fusion Output</h2>
          <p>Pixel-level alignment and semantic change analysis.</p>
        </div>
        <div className="chip-row">
          <span className="chip chip-new">New</span>
          <span className="chip chip-removed">Removed</span>
          <span className="chip chip-unchanged">Unchanged</span>
        </div>
      </div>
      <div className="result-stage">
        <img src={apiUrl(metrics.urls?.fusion)} alt="Temporal fusion output" />
        <div className="map-controls">
          <button type="button" aria-label="Zoom in"><Plus size={18} /></button>
          <button type="button" aria-label="Zoom out"><Minus size={18} /></button>
          <button type="button" aria-label="Layers"><Layers size={18} /></button>
        </div>
        <div className="map-hud">
          <div><span>Confidence</span><strong>{Math.round((metrics.confidence || 0) * 100)}%</strong></div>
          <div><span>Changed Objects</span><strong>{metrics.changed}</strong></div>
        </div>
      </div>
    </section>
  );
}

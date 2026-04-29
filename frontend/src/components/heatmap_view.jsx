import React from "react";
import { apiUrl } from "../services/api.js";
import { ImageCard } from "./image_viewer.jsx";

export default function HeatmapStage({ metrics }) {
  return (
    <section className="result-frame">
      <div className="frame-head">
        <div>
          <h2>Change Density Heatmap</h2>
          <p>Density layer for new and removed detections.</p>
        </div>
        <div className="heatmap-legend"><span>Low</span><i /><span>High</span></div>
      </div>
      <ImageCard title="Change Density Heatmap" src={apiUrl(metrics.urls?.heatmap)} />
    </section>
  );
}

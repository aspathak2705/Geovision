import React from "react";
import PageHeader from "../components/PageHeader.jsx";

export default function AboutPage() {
  const steps = [
    ["Input Alignment", "The comparison image is resized to the baseline dimensions for pixel-consistent processing."],
    ["YOLO Detection", "The building detector extracts object bounding boxes from both temporal images."],
    ["Temporal Fusion", "IoU, centroid distance, and neighbor similarity classify new, removed, and unchanged features."],
    ["Reporting Outputs", "Detection images, fusion overlays, heatmaps, and metrics JSON are written to the outputs folder."],
  ];

  return (
    <>
      <PageHeader
        kicker="System Architecture"
        title="Methodology & Processing Pipeline"
        copy="GeoVision transforms raw satellite imagery into detection layers, temporal change categories, heatmaps, and dashboard-ready metrics."
      />
      <div className="about-grid">
        <section className="card">
          {steps.map(([title, copy], index) => (
            <div className="pipeline-step" key={title}>
              <span>{index + 1}</span>
              <div><strong>{title}</strong><p>{copy}</p></div>
            </div>
          ))}
        </section>
        <section className="stack-card">
          <h2>Technical Stack</h2>
          <p><strong>Core Logic</strong><span>Python / OpenCV</span></p>
          <p><strong>Detection</strong><span>Ultralytics YOLO</span></p>
          <p><strong>Frontend</strong><span>React / HTML / CSS</span></p>
          <p><strong>Backend</strong><span>FastAPI / Render</span></p>
        </section>
      </div>
    </>
  );
}

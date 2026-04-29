import React from "react";

export const defaultMetrics = {
  new: 0,
  removed: 0,
  unchanged: 0,
  total: 0,
  changed: 0,
  change_percent: 0,
  confidence: 0,
  iou_threshold: 0,
  urls: {},
};

export function MetricCard({ label, value, note, chip, tone = "unchanged" }) {
  return (
    <article className="metric-card">
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      <p>{note}</p>
      <span className={`chip chip-${tone}`}>{chip}</span>
    </article>
  );
}

export function Insight({ title, copy, tone = "green" }) {
  return (
    <div className={`insight ${tone}`}>
      <strong>{title}</strong>
      <p>{copy}</p>
    </div>
  );
}

export function downloadReport(metrics) {
  const lines = [
    "GeoVision Satellite Change Analytics Report",
    "",
    `New detections: ${metrics.new}`,
    `Removed detections: ${metrics.removed}`,
    `Unchanged detections: ${metrics.unchanged}`,
    `Total detections: ${metrics.total}`,
    `Change percentage: ${metrics.change_percent.toFixed(2)}%`,
    `Confidence threshold: ${metrics.confidence.toFixed(2)}`,
    `IoU threshold: ${metrics.iou_threshold.toFixed(2)}`,
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "geovision_report.txt";
  anchor.click();
  URL.revokeObjectURL(url);
}

import React from "react";
import { useState } from "react";
import { Activity, History, Satellite } from "lucide-react";
import PageHeader from "../components/PageHeader.jsx";
import { Slider, UploadTile } from "../components/uploader.jsx";
import { runAnalysis } from "../services/api.js";

export default function UploadPage({ setMetrics, setActivePage, setNotice }) {
  const [t1, setT1] = useState(null);
  const [t2, setT2] = useState(null);
  const [confidence, setConfidence] = useState(0.6);
  const [iouThreshold, setIouThreshold] = useState(0.3);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState("");

  async function handleRunAnalysis() {
    setError("");
    setNotice("");

    if (!t1 || !t2) {
      setError("Please upload both t1 and t2 satellite images before running analysis.");
      return;
    }

    setIsRunning(true);
    try {
      const data = await runAnalysis({ t1, t2, confidence, iouThreshold });
      setMetrics(data.metrics);
      setActivePage("results");
    } catch (exc) {
      setError(exc.message);
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <>
      <PageHeader
        kicker="Upload & Input"
        title="Satellite Change Analysis"
        copy="Upload baseline and comparison imagery, tune detection parameters, and execute the shared GeoVision pipeline."
      />
      <div className="upload-grid">
        <UploadTile
          icon={Satellite}
          title="Satellite Image t1"
          copy="Baseline imagery (GeoTIFF, PNG, JPEG)"
          file={t1}
          onChange={setT1}
        />
        <UploadTile
          icon={History}
          title="Satellite Image t2"
          copy="Comparison imagery (GeoTIFF, PNG, JPEG)"
          file={t2}
          onChange={setT2}
        />
      </div>
      <div className="control-grid">
        <section className="card">
          <h2>Analysis Configuration</h2>
          <Slider label="Confidence threshold" min={0.1} max={0.95} step={0.05} value={confidence} onChange={setConfidence} />
          <Slider label="Matching sensitivity" min={0.1} max={0.8} step={0.05} value={iouThreshold} onChange={setIouThreshold} />
          <p className="muted">
            Higher confidence reduces low-probability detections. Higher matching sensitivity requires tighter temporal alignment.
          </p>
        </section>
        <section className="card action-card">
          <h2>Ready to Process</h2>
          <p className="muted">Runs YOLO detection, temporal fusion, heatmap generation, and metrics export.</p>
          {error ? <div className="error">{error}</div> : null}
          <button className="primary-button" onClick={handleRunAnalysis} disabled={isRunning} type="button">
            <Activity size={18} />
            {isRunning ? "Running Analysis..." : "Run Analysis"}
          </button>
        </section>
      </div>
    </>
  );
}

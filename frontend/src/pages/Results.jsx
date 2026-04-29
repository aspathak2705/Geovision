import React from "react";
import { BarChart3 } from "lucide-react";
import EmptyState from "../components/EmptyState.jsx";
import HeatmapStage from "../components/heatmap_view.jsx";
import { FusionStage, ImageCard } from "../components/image_viewer.jsx";
import PageHeader from "../components/PageHeader.jsx";
import { apiUrl } from "../services/api.js";

export default function ResultsPage({ metrics, setActivePage }) {
  if (!metrics) {
    return <EmptyState icon={BarChart3} title="No analysis run in this session" action={() => setActivePage("upload")} />;
  }

  return (
    <>
      <PageHeader
        kicker="Detection & Fusion Results"
        title="Temporal Fusion Output"
        copy="Comparative detection views, semantic change overlays, and change-density heatmap layers generated from project imagery."
      />
      <div className="result-grid">
        <ImageCard title="t1 Detection Cluster" src={apiUrl(metrics.urls?.detect_t1)} caption="Baseline detection layer" />
        <ImageCard title="t2 Detection Cluster" src={apiUrl(metrics.urls?.detect_t2)} caption="Comparison detection layer" />
      </div>
      <FusionStage metrics={metrics} />
      <HeatmapStage metrics={metrics} />
    </>
  );
}

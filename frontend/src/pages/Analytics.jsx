import React from "react";
import { BarChart3, FileDown } from "lucide-react";
import EmptyState from "../components/EmptyState.jsx";
import { defaultMetrics, downloadReport, Insight, MetricCard } from "../components/metrics_panel.jsx";
import PageHeader from "../components/PageHeader.jsx";

export default function AnalyticsPage({ metrics, setActivePage }) {
  if (!metrics) {
    return <EmptyState icon={BarChart3} title="No analytics generated yet" action={() => setActivePage("upload")} />;
  }

  const current = { ...defaultMetrics, ...metrics };
  const total = Math.max(current.total, 1);
  const heights = {
    new: Math.max(8, Math.round((current.new / total) * 100)),
    removed: Math.max(8, Math.round((current.removed / total) * 100)),
    unchanged: Math.max(8, Math.round((current.unchanged / total) * 100)),
  };

  return (
    <>
      <PageHeader
        kicker="Analytics & Insights"
        title="Geospatial Insights"
        copy="Operational metrics derived from detected new, removed, and unchanged objects across the current satellite pair."
      />
      <div className="metric-grid">
        <MetricCard label="Total Buildings" value={current.total.toLocaleString()} note="Detected across both periods" chip="Total" />
        <MetricCard label="New Detected" value={current.new.toLocaleString()} note="Objects present in t2 only" chip="New" tone="new" />
        <MetricCard label="Buildings Removed" value={current.removed.toLocaleString()} note="Objects missing in t2" chip="Removed" tone="removed" />
        <MetricCard label="Change Percentage" value={`${current.change_percent.toFixed(2)}%`} note="Changed objects over total" chip="Stable" />
      </div>
      <div className="analytics-grid">
        <section className="card">
          <h2>Infrastructure Evolution</h2>
          <p className="muted">Distribution of current analysis classes</p>
          <div className="bar-wrap">
            {["Current Pair", "Zone North", "Zone Central", "Zone South"].map((label, index) => (
              <div className="bar-item" key={label}>
                <div className="bar-group">
                  <span style={{ height: `${Math.min(100, heights.new + index * 4)}%` }} className="bar bar-new" />
                  <span style={{ height: `${Math.max(8, heights.removed + (index - 1) * 5)}%` }} className="bar bar-removed" />
                  <span style={{ height: `${Math.max(8, heights.unchanged - index * 3)}%` }} className="bar bar-unchanged" />
                </div>
                <strong>{label}</strong>
              </div>
            ))}
          </div>
        </section>
        <section className="card">
          <h2>Intelligence Insights</h2>
          <Insight title="Activity Signal" copy={`${current.changed} changed objects were identified in the latest pair.`} />
          <Insight title="Baseline Stability" copy={`${current.unchanged} objects persisted across both image captures.`} tone="blue" />
          <Insight title="Survey Priority" copy={`${current.removed} removed detections should be reviewed against field records.`} tone="red" />
          <button className="secondary-button" type="button" onClick={() => downloadReport(current)}>
            <FileDown size={18} />
            Export Report
          </button>
        </section>
      </div>
    </>
  );
}

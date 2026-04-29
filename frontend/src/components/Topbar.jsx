import React from "react";

export default function Topbar({ metrics, isLoading }) {
  return (
    <header className="topbar">
      <div className="brand">
        <div className="logo">GV</div>
        <div>
          <p className="title">GeoVision</p>
          <p className="subtitle">Satellite Change Analytics</p>
        </div>
      </div>
      <div className="status-pill">
        <span className="status-dot" />
        {isLoading ? "Connecting" : metrics ? "System Ready" : "Awaiting Analysis"}
      </div>
    </header>
  );
}

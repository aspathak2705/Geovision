import React from "react";
import { BarChart3, CloudUpload, Eye, HelpCircle, Home, Info, Settings } from "lucide-react";

const navItems = [
  { id: "home", label: "Home", icon: Home },
  { id: "upload", label: "Upload", icon: CloudUpload },
  { id: "results", label: "Results", icon: Eye },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
  { id: "about", label: "About", icon: Info },
];

export default function Sidebar({ activePage, setActivePage, hasMetrics }) {
  return (
    <aside className="sidebar">
      <div className="side-brand">
        <div className="side-title">GeoVision</div>
        <div className="side-subtitle">Intelligence Suite</div>
      </div>
      <nav className="nav-list">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              className={`nav-item ${activePage === item.id ? "active" : ""}`}
              key={item.id}
              onClick={() => setActivePage(item.id)}
              type="button"
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
      <div className={`session-state ${hasMetrics ? "ready" : ""}`}>
        <span className="status-dot" />
        {hasMetrics ? "Current session analysis ready" : "Upload images and run analysis"}
      </div>
      <div className="side-footer">
        <button type="button"><Settings size={17} />Settings</button>
        <button type="button"><HelpCircle size={17} />Help</button>
      </div>
    </aside>
  );
}

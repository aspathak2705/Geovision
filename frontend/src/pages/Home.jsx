import React from "react";
import { BarChart3, CloudUpload, Eye, Info } from "lucide-react";
import PageHeader from "../components/PageHeader.jsx";

export default function HomePage() {
  const cards = [
    { icon: CloudUpload, title: "Upload Input", copy: "Prepare temporal satellite images for analysis." },
    { icon: Eye, title: "Results Visualization", copy: "Inspect detection, fusion, and heatmap outputs." },
    { icon: BarChart3, title: "Analytics Insights", copy: "Review metrics and derived intelligence signals." },
    { icon: Info, title: "System Methodology", copy: "Understand the processing pipeline." },
  ];

  return (
    <>
      <PageHeader
        kicker="Dashboard Structure"
        title="GeoVision Intelligence Suite"
        copy="Use the sidebar pages to upload imagery, run detection, inspect fusion outputs, review analytics, and read the project methodology."
      />
      <div className="metric-grid feature-grid">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <article className="metric-card" key={card.title}>
              <Icon className="feature-icon" size={25} />
              <h3>{card.title}</h3>
              <p>{card.copy}</p>
            </article>
          );
        })}
      </div>
    </>
  );
}

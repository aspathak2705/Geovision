import React from "react";
import { CloudUpload } from "lucide-react";

export default function EmptyState({ icon: Icon, title, action }) {
  return (
    <section className="empty-state">
      <Icon size={44} />
      <h2>{title}</h2>
      <p>Upload images and click Run Analysis to generate detection, fusion, heatmap, and analytics outputs.</p>
      <button className="secondary-button" type="button" onClick={action}>
        <CloudUpload size={18} />
        Go to Upload
      </button>
    </section>
  );
}

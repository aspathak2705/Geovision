import React from "react";

export default function PageHeader({ kicker, title, copy }) {
  return (
    <section className="page-header">
      <div className="page-kicker">{kicker}</div>
      <h1>{title}</h1>
      <p>{copy}</p>
    </section>
  );
}

import React from "react";
import { useEffect, useMemo, useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import Topbar from "./components/Topbar.jsx";
import AboutPage from "./pages/About.jsx";
import AnalyticsPage from "./pages/Analytics.jsx";
import HomePage from "./pages/Home.jsx";
import ResultsPage from "./pages/Results.jsx";
import UploadPage from "./pages/Upload.jsx";
import { fetchMetrics } from "./services/api.js";

export default function App() {
  const [activePage, setActivePage] = useState("home");
  const [metrics, setMetrics] = useState(null);
  const [isLoadingMetrics, setIsLoadingMetrics] = useState(true);
  const [notice, setNotice] = useState("");

  useEffect(() => {
    fetchMetrics()
      .then((data) => setMetrics(data.metrics))
      .catch(() => setNotice("Backend is not connected yet. Set VITE_API_BASE_URL to your Render API URL."))
      .finally(() => setIsLoadingMetrics(false));
  }, []);

  const page = useMemo(() => {
    switch (activePage) {
      case "upload":
        return <UploadPage setMetrics={setMetrics} setActivePage={setActivePage} setNotice={setNotice} />;
      case "results":
        return <ResultsPage metrics={metrics} setActivePage={setActivePage} />;
      case "analytics":
        return <AnalyticsPage metrics={metrics} setActivePage={setActivePage} />;
      case "about":
        return <AboutPage />;
      default:
        return <HomePage />;
    }
  }, [activePage, metrics]);

  return (
    <div className="app-shell">
      <Sidebar activePage={activePage} setActivePage={setActivePage} hasMetrics={Boolean(metrics)} />
      <main className="content">
        <Topbar metrics={metrics} isLoading={isLoadingMetrics} />
        {notice ? <div className="notice">{notice}</div> : null}
        {page}
      </main>
    </div>
  );
}

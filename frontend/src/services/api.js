export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

export function apiUrl(path) {
  if (!path) return "";
  return path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
}

export async function fetchMetrics() {
  const response = await fetch(`${API_BASE_URL}/api/metrics`);
  if (!response.ok) {
    throw new Error("Unable to load metrics.");
  }
  return response.json();
}

export async function runAnalysis({ t1, t2, confidence, iouThreshold }) {
  const formData = new FormData();
  formData.append("t1", t1);
  formData.append("t2", t2);
  formData.append("confidence", String(confidence));
  formData.append("iou_threshold", String(iouThreshold));

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Analysis failed.");
  }

  return data;
}

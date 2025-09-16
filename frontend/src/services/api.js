const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export const api = {
  async getWorldBankIndicator(country = "FRA", indicator = "NY.GDP.MKTP.CD") {
    const response = await fetch(
      `${API_BASE}/api/worldbank/indicator?country=${country}&indicator=${indicator}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  async getFredSeries(seriesId = "UNRATE") {
    const response = await fetch(
      `${API_BASE}/api/fred/series?series_id=${seriesId}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  async healthCheck() {
    const response = await fetch(`${API_BASE}/healthz`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }
};

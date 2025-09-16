const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export const api = {
  async getExampleData() {
    const response = await fetch(`${API_BASE}/api/example/data`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  async getExternalData(url) {
    const response = await fetch(`${API_BASE}/api/example/external?url=${encodeURIComponent(url)}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  },

  async processData(data) {
    const response = await fetch(`${API_BASE}/api/example/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
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

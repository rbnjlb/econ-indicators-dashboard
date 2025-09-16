import { useEffect, useState } from "react";
import Chart from "./components/Chart";
import { api } from "./services/api";

export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const result = await api.getWorldBankIndicator("FRA", "NY.GDP.MKTP.CD");
        setData(result.data || []);
      } catch (e) {
        setError(String(e));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <p>Loading…</p>;
  if (error) return <p style={{ color: "crimson" }}>Error: {error}</p>;

  return (
    <div style={{ fontFamily: "Inter, system-ui, sans-serif", padding: 24 }}>
      <h1>Economic Indicators Dashboard</h1>
      <Chart 
        data={data} 
        title="GDP (current US$) — World Bank (FRA)"
        dataKey="value"
        xAxisKey="year"
      />
    </div>
  );
}
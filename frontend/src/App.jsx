import { useEffect, useState } from "react";
import Chart from "./components/Chart";
import DataTable from "./components/DataTable";
import { api } from "./services/api";

export default function App() {
  const [exampleData, setExampleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const result = await api.getExampleData();
        setExampleData(result.data || []);
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
      <h1>Generic Dashboard Template</h1>
      <p>This is a generic template that you can customize for your project.</p>
      
      <DataTable 
        data={exampleData} 
        title="Example Data Table"
      />
      
      <Chart 
        data={exampleData} 
        title="Example Chart (Line)"
        dataKey="value"
        xAxisKey="name"
        type="line"
      />
      
      <Chart 
        data={exampleData} 
        title="Example Chart (Bar)"
        dataKey="value"
        xAxisKey="name"
        type="bar"
      />
    </div>
  );
}
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, BarChart, Bar } from "recharts";

export default function Chart({ data, title, dataKey = "value", xAxisKey = "year", type = "line" }) {
  const renderChart = () => {
    if (type === "bar") {
      return (
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} />
          <YAxis />
          <Tooltip />
          <Bar dataKey={dataKey} fill="#8884d8" />
        </BarChart>
      );
    }
    
    return (
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={xAxisKey} />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey={dataKey} dot={false} stroke="#8884d8" />
      </LineChart>
    );
  };

  return (
    <div style={{ width: "100%", height: 420 }}>
      <h3>{title}</h3>
      <ResponsiveContainer>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
}

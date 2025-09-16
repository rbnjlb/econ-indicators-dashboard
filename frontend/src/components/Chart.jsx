import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function Chart({ data, title, dataKey = "value", xAxisKey = "year" }) {
  return (
    <div style={{ width: "100%", height: 420 }}>
      <h3>{title}</h3>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey={dataKey} dot={false} stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

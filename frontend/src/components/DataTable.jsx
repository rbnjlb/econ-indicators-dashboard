export default function DataTable({ data, title }) {
  if (!data || data.length === 0) {
    return (
      <div style={{ padding: 20 }}>
        <h3>{title}</h3>
        <p>No data available</p>
      </div>
    );
  }

  const columns = Object.keys(data[0]);

  return (
    <div style={{ padding: 20 }}>
      <h3>{title}</h3>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ 
          width: '100%', 
          borderCollapse: 'collapse',
          border: '1px solid #ddd'
        }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5' }}>
              {columns.map((column, index) => (
                <th 
                  key={index}
                  style={{ 
                    padding: '12px', 
                    textAlign: 'left',
                    border: '1px solid #ddd'
                  }}
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columns.map((column, colIndex) => (
                  <td 
                    key={colIndex}
                    style={{ 
                      padding: '12px',
                      border: '1px solid #ddd'
                    }}
                  >
                    {row[column]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

import './table.css';
import { useState, useEffect } from 'react';

export const Table = ({ rows }) => {
  const [sortedRows, setRows] = useState([]);

  useEffect(() => {
    if (rows) {
      setRows(rows);
    }
  }, [rows]);

  if (!rows || rows.length === 0) {
    return <p>No data available</p>;
  }

  return (
  <div className="table-container">
    <table>
      <thead>
        <tr>
          {Object.keys(rows[0]).map((entry, index) => (
            <th key={index}>{entry}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sortedRows.map((row, index) => (
          <tr key={index}>
            {Object.values(row).map((entry, columnIndex) => (
              <td key={columnIndex}>{entry}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
  );
};

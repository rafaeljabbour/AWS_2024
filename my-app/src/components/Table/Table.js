import './table.css';
import { useState, useEffect } from 'react';

export const Table = ({ rows }) => {
  const [sortedRows, setRows] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredRows, setFilteredRows] = useState([]);

  useEffect(() => {
    if (rows) {
      setRows(rows);
      setFilteredRows(rows);
    }
  }, [rows]);

  const handleSearch = async (event) => {
    const term = event.target.value;
    setSearchTerm(term);

    if (term.trim() === '') {
      setFilteredRows(sortedRows);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchTerm: term }),
      });

      const data = await response.json();
      const filtered = sortedRows.filter(row =>
        Object.values(row).some(value =>
          data.some(phrase => value.toString().toLowerCase().includes(phrase.toLowerCase()))
        )
      );

      setFilteredRows(filtered);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  if (!rows || rows.length === 0) {
    return <p>No data available</p>;
  }

  return (
    <div className="table-container">
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-input"
      />
      <table>
        <thead>
          <tr>
            {Object.keys(rows[0]).map((entry, index) => (
              <th key={index}>{entry}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filteredRows.map((row, index) => (
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

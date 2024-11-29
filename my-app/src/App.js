import './App.css';
import { useState, useEffect } from 'react';
import { Table } from './components/Table/Table';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch data from example_events.json
    fetch('./public/example_events.json')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <Table rows={data} />
    </div>
  );
}

export default App;

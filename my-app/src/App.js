import './App.css';
import { Table } from './components/Table/Table.js';
import {data} from './data.js'

function App() {
  return (
    <div>
      <Table rows={data}/>
    </div>
  );
}

export default App;

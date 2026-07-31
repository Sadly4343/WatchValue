import { useState } from 'react'
import './App.css'
const emptyRow = {
  manufacturer: '',
  model: '',
  size: '',
  jewels: '',
  case_material: '',
  running_condition: '',
  sold_price: '',
  sold_date: '',
  description: '',
}
function App() {
  const [rows, setRows] = useState([
    {...emptyRow}
    
  ])
  function handleChange(rowIndex, field, value) {
  const newRows = [...rows]
  newRows[rowIndex][field] = value
  setRows(newRows)
  }

  function addRow() {
  const newArray = [...rows]
  newArray.push({
    ...emptyRow
  })
  setRows(newArray)
}



  return (
  <div>
    <div>
      <h1>Add Watch Listings</h1>
    </div>
    
    {rows.map((row, index) =>
      <div key={index}>
        <input
          type="text"
          placeholder="Manufacturer"
          value={row.manufacturer}
          onChange={(e) => handleChange(index, 'manufacturer', e.target.value)}
        />
        <input
          type="text"
          placeholder="Model"
          value={row.model}
          onChange={(e) => handleChange(index, 'model', e.target.value)}
        />
      </div>
    
    
    )}
      
  </div>
)
}

export default App
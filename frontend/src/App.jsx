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

  async function handleSubmit() {
  const response = await fetch('http://127.0.0.1:8000/listings/bulk', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(rows)
  })

  if (response.ok) {
    const data = await response.json()
    console.log("Created listings", data)
    alert('Listings created succesfully')
    setExpandedIndex(0)
    setRows([{...emptyRow}])

  } else (
    alert('Something went wrong submitting listings')
  )
}

  const [expandedIndex, setExpandedIndex] = useState(0)
  function handleChange(rowIndex, field, value) {
  const newRows = [...rows]
  newRows[rowIndex][field] = value
  setRows(newRows)
  }

  function addRow() {
  const newRows = [...rows]
  newRows.push({ ...emptyRow })
  setRows(newRows)
  setExpandedIndex(rows.length)
}


return (
  <div>
  <div>
    <h1>Add Watch Listings</h1>
  </div>

  {rows.map((row, index) => (
    <div key={index} className="row-card">
      {index === expandedIndex ? (
        <div className="row-grid">
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
          <input
            type="text"
            placeholder="Size"
            value={row.size}
            onChange={(e) => handleChange(index, 'size', e.target.value)}
          />
          <input
            type="number"
            placeholder="Jewels"
            value={row.jewels}
            onChange={(e) => handleChange(index, 'jewels', e.target.value)}
          />
          <input
            type="text"
            placeholder="Case Material"
            value={row.case_material}
            onChange={(e) => handleChange(index, 'case_material', e.target.value)}
          />
          <input
            type="text"
            placeholder="Running Condition"
            value={row.running_condition}
            onChange={(e) => handleChange(index, 'running_condition', e.target.value)}
          />
          <input
            type="number"
            placeholder="Sold Price"
            value={row.sold_price}
            onChange={(e) => handleChange(index, 'sold_price', e.target.value)}
          />
          <input
            type="date"
            placeholder="Sold Date"
            value={row.sold_date}
            onChange={(e) => handleChange(index, 'sold_date', e.target.value)}
          />
          <textarea
            placeholder="Description"
            className="full-width"
            value={row.description}
            onChange={(e) => handleChange(index, 'description', e.target.value)}
          />
        </div>
      ) : (
        <div onClick={() => setExpandedIndex(index)}>
          {row.manufacturer} — {row.model} — ${row.sold_price}
        </div>
      )}
    </div>
  ))}

  <button className="add-row-btn" onClick={addRow}>+ Add another watch</button>
  <button className="add-row-btn" onClick={handleSubmit}>Send</button>
</div>
)
}
export default App
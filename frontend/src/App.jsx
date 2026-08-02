import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
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
  const [rows, setRows] = useState([{ ...emptyRow }])
  const [expandedIndex, setExpandedIndex] = useState(0)
  const [watchQuestion, setWatchQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

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

  async function handleSubmit() {
    const response = await fetch('http://127.0.0.1:8000/listings/bulk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(rows),
    })

    if (response.ok) {
      const data = await response.json()
      console.log('Created listings', data)
      alert('Listings created successfully')
      setExpandedIndex(0)
      setRows([{ ...emptyRow }])
    } else {
      alert('Something went wrong submitting listings')
    }
  }

  async function handleSearch() {
    setIsLoading(true)

    const response = await fetch(
      `http://127.0.0.1:8000/generation/?question=${encodeURIComponent(watchQuestion)}`
    )

    if (response.ok) {
      const data = await response.json()
      setResult(data)
    } else {
      alert('Something went wrong with the search.')
    }

    setIsLoading(false)
  }

  return (
    <div className="app">
      <div>
        <h1>Watch Valuation Search</h1>
        <input
          type="text"
          placeholder="Ask a question, e.g. 'fair price for a Waltham Vanguard 16 size'"
          value={watchQuestion}
          onChange={(e) => setWatchQuestion(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>

        {isLoading && <p>Searching...</p>}

        {result && (
          <div className="result-box">
            <ReactMarkdown>{result.answer}</ReactMarkdown>
            <p>
              Average: ${result.price_stats.avg} | Range: ${result.price_stats.min} - $
              {result.price_stats.max} | Based on {result.price_stats.count} sales
            </p>

            <div>
              <h3>Sources</h3>
              {result.matches.map((match, index) => (
                <p key={index}>{match.chunk_text}</p>
              ))}
            </div>
          </div>
        )}
      </div>

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

      <button className="add-row-btn" onClick={addRow}>
        + Add another watch
      </button>
      <button className="add-row-btn" onClick={handleSubmit}>
        Send
      </button>
    </div>
  )
}

export default App
// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [fromDate, setFromDate] = useState('2025-01-01');
  const [toDate, setToDate] = useState('2025-07-10');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const params = {
        ticker,
        from: fromDate,
        to: toDate
      };
      const resp = await axios.get('http://localhost:8000/api/analyze', { params });
      setResult(resp.data);
    } catch (e) {
      setError('Something went wrong! Please check your backend and parameters.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Quant Alpha Dashboard (Basic)</h1>
      <div style={{ marginBottom: 20 }}>
        <input value={ticker} onChange={e => setTicker(e.target.value.toUpperCase())} />
        <input type="date" value={fromDate} onChange={e => setFromDate(e.target.value)} />
        <input type="date" value={toDate} onChange={e => setToDate(e.target.value)} />
        <button onClick={handleAnalyze} disabled={loading}>Analyze</button>
      </div>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {result && (
        <div style={{ textAlign: 'left', marginTop: 20 }}>
          <h3>API Result</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

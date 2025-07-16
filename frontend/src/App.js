import React, { useState } from 'react';
import axios from 'axios';

function App() {
  // State for single ticker analysis
  const [ticker, setTicker] = useState('AAPL');
  const [fromDate, setFromDate] = useState('2025-01-01');
  const [toDate, setToDate] = useState('2025-07-10');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // State for portfolio analysis
  const [holdings, setHoldings] = useState([
    { ticker: '', shares: '', cost: '', date: '' }
  ]);

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

  // --- Formatting helpers ---
  const formatNumber = (n) => (typeof n === 'number' ? n.toFixed(4) : n);

  // --- Sample styles ---
  const mainStyle = {
    maxWidth: 700,
    margin: '48px auto',
    padding: 32,
    background: "#f6f8fa",
    borderRadius: 18,
    boxShadow: "0 2px 18px rgba(0,0,0,0.09)",
    fontFamily: 'Inter, Segoe UI, Arial, sans-serif'
  };

  const cardStyle = {
    background: "#fff",
    borderRadius: 12,
    padding: 24,
    boxShadow: "0 2px 8px rgba(51,70,128,0.07)",
    marginBottom: 28
  };

  const labelStyle = {
    fontSize: "0.98em", 
    fontWeight: 500, 
    marginBottom: 5, 
    display: 'block'
  };

  const inputStyle = {
    padding: "8px 10px",
    borderRadius: 6,
    border: "1px solid #ccd6e0",
    marginRight: 10,
    marginBottom: 0
  };

  const buttonStyle = {
    background: "#425bef",
    color: "#fff",
    fontWeight: 600,
    border: "none",
    borderRadius: 8,
    padding: "10px 24px",
    cursor: "pointer",
    marginLeft: 8
  };

  // Portfolio handlers
  const handleHoldingChange = (i, field, value) => {
    const next = [...holdings];
    next[i][field] = value;
    setHoldings(next);
  };

  const addHolding = () => setHoldings([...holdings, { ticker: '', shares: '', cost: '', date: '' }]);
  const removeHolding = i => setHoldings(holdings.filter((_, idx) => idx !== i));
  const handlePortfolioAnalyze = (e) => {
    e.preventDefault();
    // Replace alert with your backend call when ready
    alert(JSON.stringify(holdings, null, 2));
  };

  return (
    <div style={mainStyle}>
      {/* App Title */}
      <h1 style={{ fontSize: '2.3rem', color: "#222c48", marginTop: 0, marginBottom: 25, textAlign: "center", letterSpacing: -1 }}>
        Investify
      </h1>

      {/* --- Portfolio Input Section --- */}
      <form onSubmit={handlePortfolioAnalyze}
        style={{
          background: "#fff",
          borderRadius: 12,
          padding: 24,
          boxShadow: "0 2px 8px rgba(51,70,128,0.07)",
          maxWidth: 700,
          margin: "30px auto"
        }}>
        <h2 style={{marginBottom: 12, color: "#20325d"}}>Analyze Your Portfolio</h2>
        {holdings.map((row, i) => (
          <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 8 }}>
            <input required placeholder="Ticker"
              value={row.ticker}
              onChange={e => handleHoldingChange(i, 'ticker', e.target.value.toUpperCase())}
              style={{ width: 80 }}
            />
            <input required type="number" min="0" step="any" placeholder="Shares"
              value={row.shares}
              onChange={e => handleHoldingChange(i, 'shares', e.target.value)}
              style={{ width: 70 }}
            />
            <input required type="number" min="0" step="any" placeholder="Cost/Share"
              value={row.cost}
              onChange={e => handleHoldingChange(i, 'cost', e.target.value)}
              style={{ width: 110 }}
            />
            <input type="date"
              value={row.date}
              onChange={e => handleHoldingChange(i, 'date', e.target.value)}
              style={{ width: 135 }}
            />
            <button type="button" onClick={() => removeHolding(i)} style={{ color: '#b00020' }}>Remove</button>
          </div>
        ))}
        <div>
          <button type="button" onClick={addHolding} style={{marginRight: 10}}>Add Row</button>
          <button type="submit" style={{background:'#304ffe', color:'#fff'}}>Analyze Portfolio</button>
        </div>
      </form>
      {/* --- Single Ticker Input Card --- */}
      {/*
<div style={cardStyle}>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 14 }}>
          <div>
            <label style={labelStyle}>Ticker</label>
            <input
              style={inputStyle}
              value={ticker}
              maxLength={6}
              onChange={e => setTicker(e.target.value.toUpperCase())}
            />
          </div>
          <div>
            <label style={labelStyle}>From</label>
            <input
              style={inputStyle}
              type="date"
              value={fromDate}
              onChange={e => setFromDate(e.target.value)}
            />
          </div>
          <div>
            <label style={labelStyle}>To</label>
            <input
              style={inputStyle}
              type="date"
              value={toDate}
              onChange={e => setToDate(e.target.value)}
            />
          </div>
          <button style={buttonStyle} onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
        {error && (
          <div style={{
            color: "#b90020",
            background: "#fff7f8",
            marginTop: 18,
            borderRadius: 8,
            border: "1px solid #fac7ce",
            padding: "10px 18px"
          }}>
            {error}
          </div>
        )}
      </div>
      */}
      
      
      
        
      {/* Results */}
      {result && (
        <div style={cardStyle}>
          <h2 style={{ color: "#20325d", fontWeight: 700, fontSize: "1.25rem", marginBottom: 10 }}>
            Model Performance
          </h2>
          <ul style={{ listStyle: "none", paddingLeft: 0, marginBottom: 22 }}>
            <li><strong>RMSE:</strong> {formatNumber(result.metrics.rmse)}</li>
            <li><strong>MAE:</strong> {formatNumber(result.metrics.mae)}</li>
            <li><strong>R²:</strong> {formatNumber(result.metrics.r2)}</li>
            <li><strong>Mean Alpha:</strong> {formatNumber(result.metrics.mean_alpha)}</li>
          </ul>
          <h2 style={{ color: "#20325d", fontWeight: 700, fontSize: "1.15rem", marginBottom: 7 }}>Raw Result</h2>
          <pre
            style={{
              background: "#f3f6fa",
              border: "1px solid #e0e6ef",
              borderRadius: 8,
              fontSize: "0.97em",
              maxHeight: 220,
              overflow: "auto",
              padding: 10
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}

      {/* Loader */}
      {loading && (
        <div style={{ textAlign: "center", color: "#425bef", marginTop: 24, fontWeight: 600 }}>
          Loading...
        </div>
      )}
    </div>
  );
}

export default App;

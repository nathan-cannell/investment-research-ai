import React, { useState } from 'react';
import axios from 'axios';

function App() {
  // Multi-stock portfolio state
  const [holdings, setHoldings] = useState([
    { ticker: '', shares: '' }
  ]);
  // Optional date range state (now included)
  const [fromDate, setFromDate] = useState('');
  // const [toDate, setToDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // Handlers for portfolio table
  const handleHoldingChange = (i, field, value) => {
    const next = [...holdings];
    next[i][field] = value;
    setHoldings(next);
  };

  const addHolding = () =>
    setHoldings([...holdings, { ticker: '', shares: '' }]);

  const removeHolding = i =>
    setHoldings(holdings.filter((_, idx) => idx !== i));

  // Handler for the analyze portfolio action
  const handlePortfolioAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    const todayStr = new Date().toISOString().slice(0,10);
    try {
      const payload = {
        holdings,
        from: fromDate,
        to: todayStr
      };
      const resp = await axios.post('http://localhost:8000/api/analyze-portfolio', payload);
      setResult(resp.data);
    } catch (e) {
      setError('Something went wrong! Please check your backend and parameters.');
    } finally {
      setLoading(false);
    }
  };

  // Styles (as before)
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

  return (
    <div style={mainStyle}>
      <h1 style={{
        fontSize: '2.3rem', color: "#222c48",
        marginTop: 0, marginBottom: 25, textAlign: "center", letterSpacing: -1
      }}>
        Investify
      </h1>

      <form onSubmit={handlePortfolioAnalyze} style={cardStyle}>
        <h2 style={{ marginBottom: 12, color: "#20325d" }}>Analyze Your Portfolio</h2>
        <p style={{ fontSize: "1em", marginBottom: 10, color: "#384760" }}>
          Enter your stocks and shares. Purchase price/date are optional.<br />
          Pick a date range (optional) for performance, or leave blank for general tips!
        </p>

        {/* Date Range Section */}
        <div style={{
          display: "flex", alignItems: 'flex-end', gap: 16, marginBottom: 18
        }}>
          <div>
            <label style={{
              fontSize: "0.98em", fontWeight: 500, marginBottom: 4, display: 'block'
            }}>From (optional)</label>
            <input
              type="date"
              value={fromDate}
              onChange={e => setFromDate(e.target.value)}
              style={{
                padding: "8px 10px", borderRadius: 6, border: "1px solid #ccd6e0", width: 140
              }}
            />
          </div>
          
        </div>

        {/* Holdings Table */}
        {holdings.map((row, i) => (
          <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 8 }}>
            <input
              required
              placeholder="Ticker"
              value={row.ticker}
              onChange={e => handleHoldingChange(i, 'ticker', e.target.value.toUpperCase())}
              style={{ width: 80, padding: "8px", borderRadius: 6, border: "1px solid #ccd6e0" }}
              maxLength={7}
            />
            <input
              required
              type="number"
              min="0"
              step="any"
              placeholder="Shares"
              value={row.shares}
              onChange={e => handleHoldingChange(i, 'shares', e.target.value)}
              style={{ width: 90, padding: "8px", borderRadius: 6, border: "1px solid #ccd6e0" }}
            />
            <button
              type="button"
              onClick={() => removeHolding(i)}
              style={{ color: '#b00020', background: "none", border: "none", fontWeight: 500, cursor: "pointer" }}
              disabled={holdings.length === 1}
            >Remove</button>
          </div>
        ))}
        <div style={{ marginBottom: 10 }}>
          <button type="button" onClick={addHolding}
            style={{
              marginRight: 10, background: "#f4f7fa", color: "#222c48",
              padding: "8px 16px", borderRadius: 7, border: "1px solid #ccd6e0"
            }}>Add Row</button>
          <button
            type="submit"
            style={{
              background: '#304ffe', color: '#fff', fontWeight: 600,
              padding: "8px 20px", borderRadius: 8, border: "none"
            }}>
            {loading ? "Analyzing..." : "Analyze Portfolio"}
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
      </form>

      {/* Placeholder for results */}
      {result && (
        <div style={cardStyle}>
          <h2 style={{ color: "#20325d", fontWeight: 700, fontSize: "1.18rem", marginBottom: 9 }}>
            Portfolio Results
          </h2>
          <pre style={{
            background: "#f3f6fa",
            border: "1px solid #e0e6ef",
            borderRadius: 8,
            fontSize: "0.97em",
            maxHeight: 260,
            overflow: "auto",
            padding: 10
          }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}

      {loading && (
        <div style={{ textAlign: "center", color: "#425bef", marginTop: 24, fontWeight: 600 }}>
          Loading...
        </div>
      )}
    </div>
  );
}

export default App;

from flask import Flask, request, jsonify
from flask_cors import CORS
from data_pipeline import OHLCV
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

@app.route('/api/analyze-portfolio', methods=['POST'])
def analyze_portfolio():
    data = request.get_json()
    holdings = data.get('holdings', [])
    from_date = data.get('from', '2025-01-01')
    to_date = datetime.now().strftime('%Y-%m-%d')
    api_key = os.environ.get("POLYGON_API_KEY", "YOUR_API_KEY")

    portfolio_results = []
    total_portfolio_value = 0
    sector_breakdown = {}

    for holding in holdings:
        ticker = holding.get('ticker', '').upper()
        shares = float(holding.get('shares', 0))
        if not ticker or shares <= 0:
            continue

        asset_df = OHLCV(api_key, ticker, from_date, to_date)
        if asset_df.empty or 'close' not in asset_df.columns:
            continue
        
        latest_close = asset_df['close'].iloc[-1]
        position_value = shares * latest_close
        total_portfolio_value += position_value
        sector = "Unknown"  # Placeholder; replace with real sector lookup if desired

        portfolio_results.append({
            'ticker': ticker,
            'shares': shares,
            'latest_close': latest_close,
            'position_value': position_value,
            'sector': sector
        })

        sector_breakdown[sector] = sector_breakdown.get(sector, 0) + position_value

    sector_allocations = {
        k: v / total_portfolio_value for k, v in sector_breakdown.items()
    } if total_portfolio_value > 0 else {}

    tips = []
    if sector_allocations:
        for sector, pct in sector_allocations.items():
            if pct > 0.35:
                tips.append(f"You have a high allocation ({pct:.0%}) in {sector}; consider rebalancing.")
            elif pct < 0.10:
                tips.append(f"Consider adding exposure to {sector} for diversification.")
    tips.append("Consider broad market ETFs or underweighted sector index funds for better diversification.")

    response = {
        'portfolio_value': total_portfolio_value,
        'holdings': portfolio_results,
        'sector_allocations': sector_allocations,
        'tips': tips
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

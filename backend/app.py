from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['GET'])
def analyze():
    # Get parameters from frontend (with default fallback)
    ticker = request.args.get('ticker', 'AAPL')
    start = request.args.get('from', '2025-01-01')
    end = request.args.get('to', '2025-07-10')

    # Dummy output; replace with real analytic results
    result = {
        "ticker": ticker,
        "from": start,
        "to": end,
        "message": f"Received request for {ticker} from {start} to {end}.",
        "metrics": {
            "rmse": 1.23,
            "mae": 0.45,
            "r2": 0.98,
            "mean_alpha": 0.0042
        },
        "predicted": [125, 127, 126, 129, 128, 130],
        "actual": [124, 126, 127, 128, 128, 131],
        "dates": [
            "2025-01-01", "2025-01-02", "2025-01-03",
            "2025-01-04", "2025-01-05", "2025-01-06"
        ],
        "feature_labels": ["SMA_10", "SMA_20", "RSI_14"],
        "feature_scores": [0.6, 0.2, 0.2]
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

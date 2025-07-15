# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from data_pipeline import OHLCV, base_returns
from xgboost_model import (
    prepare_features_targets, train_xgboost, predict_xgboost, compute_strategy_alpha
)
import os

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

@app.route('/api/analyze', methods=['GET'])
def analyze():
    # Collect user parameters from frontend
    ticker = request.args.get('ticker', 'AAPL')
    from_date = request.args.get('from', '2025-01-01')
    to_date = request.args.get('to', '2025-07-10')
    api_key = os.environ.get("POLYGON_API_KEY", "YOUR_API_KEY")

    # 1. Fetch and prepare data
    asset_df = OHLCV(api_key, ticker, from_date, to_date)
    benchmark_df, _ = base_returns(api_key, "SPY", from_date, to_date)
    if asset_df.empty or benchmark_df.empty:
        return jsonify({'error': 'No data found'}), 400

    # 2. Feature engineering for XGBoost
    features, targets, lagged_df = prepare_features_targets(asset_df, 'close', 5)
    lagged_df['benchmark_return'] = benchmark_df['close'].reindex(lagged_df.index).pct_change()

    # 3. Train/Test split
    split_idx = int(len(features) * 0.8)
    X_train, X_test = features.iloc[:split_idx], features.iloc[split_idx:]
    y_train, y_test = targets.iloc[:split_idx], targets.iloc[split_idx:]

    # 4. Train and evaluate XGBoost
    model = train_xgboost(X_train, y_train)
    y_pred = predict_xgboost(model, X_test)
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    lagged_test = lagged_df.loc[X_test.index]
    strategy_result, mean_alpha = compute_strategy_alpha(lagged_test, y_pred, benchmark_col='close')

    # 5. Prepare JSON response
    resp = {
        'metrics': {
            'rmse': rmse, 'mae': mae, 'r2': r2, 'mean_alpha': mean_alpha
        },
        'predicted': y_pred.tolist(),
        'actual': y_test.tolist(),
        'dates': [str(idx) for idx in y_test.index],
        'feature_labels': list(X_train.columns),
        'feature_scores': model.feature_importances_.tolist()
    }
    return jsonify(resp)

if __name__ == "__main__":
    app.run(debug=True, port=8000)

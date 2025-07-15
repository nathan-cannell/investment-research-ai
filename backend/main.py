# main.py

import pandas as pd
from data_pipeline import OHLCV, base_returns
from xgboost_model import (
    prepare_features_targets,
    train_xgboost,
    predict_xgboost,
    compute_strategy_alpha,
    plot_feature_importance,
    plot_predicted_vs_actual,
    evaluate_model_full
)
import os
from dotenv import load_dotenv

def main():
    load_dotenv()  # loads variables from your .env file into the environment
    API_KEY = os.environ.get('POLYGON_API_KEY')
    if API_KEY is None:
        raise ValueError("POLYGON_API_KEY environment variable not set.")
    from_date = "2025-01-01"
    to_date = "2025-07-10"

    # Step 1: Data Ingestion
    asset_ticker = "AAPL"
    benchmark_ticker = "SPY"
    asset_df = OHLCV(API_KEY, asset_ticker, from_date, to_date)
    benchmark_df, _ = base_returns(API_KEY, benchmark_ticker, from_date, to_date)

    # Sanity check
    if asset_df.empty:
        raise ValueError("Failed to fetch asset data.")
    if benchmark_df.empty:
        raise ValueError("Failed to fetch benchmark data.")

    # Step 2: Feature Engineering (lagged features + technicals)
    features, targets, lagged_df = prepare_features_targets(asset_df, target_col='close', lags=5)

    # Align with available benchmark returns (optional, ensures equal sample)
    lagged_df['benchmark_return'] = benchmark_df['close'].reindex(lagged_df.index).pct_change(fill_method=None)


    # Step 3: Train-Test Split (no shuffle for time series)
    split_idx = int(len(features) * 0.8)
    X_train, X_test = features.iloc[:split_idx], features.iloc[split_idx:]
    y_train, y_test = targets.iloc[:split_idx], targets.iloc[split_idx:]

    # Step 4: Train Model
    model = train_xgboost(X_train, y_train)

    # Step 5: Predict on Test Set
    y_pred = predict_xgboost(model, X_test)


    metrics = evaluate_model_full(y_test, y_pred, label="XGBoost")
    plot_predicted_vs_actual(y_test.values, y_pred, index=y_test.index, label="Close Price")


    # Step 6: Compute Alpha (strategy vs. buy & hold)
    lagged_test = lagged_df.loc[X_test.index]
    strategy_result, mean_alpha = compute_strategy_alpha(
        lagged_test, y_pred, benchmark_col='close'
    )

    # Step 7: Display Results
    print("=" * 40)
    print("Model Performance Metrics:")
    print(f"Test RMSE: {((y_test - y_pred) ** 2).mean() ** 0.5:.4f}")
    print(f"Mean Strategy Alpha (out-of-sample): {mean_alpha:.4%}")

    # Show last 5 predictions
    print(strategy_result[['timestamp', 'close', 'predicted_close', 
                          'strategy_return', 'benchmark_return', 'alpha']].tail())

    # Step 8: Feature Importance
    plot_feature_importance(model, X_train.columns)

if __name__ == "__main__":
    main()

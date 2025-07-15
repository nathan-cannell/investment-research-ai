# xgboost_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def create_lagged_features(df, target_col='close', lags=5, drop_missing=True):
    """Create lagged features for supervised learning with time series data."""
    new_df = df.copy()
    for lag in range(1, lags + 1):
        new_df[f'{target_col}_lag_{lag}'] = new_df[target_col].shift(lag)
    if drop_missing:
        new_df = new_df.dropna()
    return new_df

def add_technical_indicators(df):
    """Add simple technical indicators used for return/alpha predictive modeling."""
    new_df = df.copy()
    # Moving Averages
    new_df['SMA_10'] = new_df['close'].rolling(window=10).mean()
    new_df['SMA_20'] = new_df['close'].rolling(window=20).mean()
    # Daily Return
    new_df['return'] = new_df['close'].pct_change()
    # Relative Strength Index (RSI)
    delta = new_df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-6)
    new_df['RSI_14'] = 100 - (100 / (1 + rs))
    new_df = new_df.dropna()
    return new_df

def prepare_features_targets(df, target_col='close', lags=5):
    """Generate feature matrix X and target vector y for train/test split."""
    feat_df = add_technical_indicators(df)
    lagged_df = create_lagged_features(feat_df, target_col=target_col, lags=lags)
    features = lagged_df.drop(['timestamp', target_col], axis=1, errors='ignore')
    targets = lagged_df[target_col]
    return features, targets, lagged_df

def train_xgboost(X_train, y_train, params=None):
    """Train XGBoost model for regression."""
    if params is None:
        params = {
            'objective': 'reg:squarederror',
            'n_estimators': 300,
            'learning_rate': 0.03,
            'max_depth': 4,
            'subsample': 0.7,
            'colsample_bytree': 0.7,
            'random_state': 42
        }
    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train)
    return model

def predict_xgboost(model, X):
    """Run inference using a trained XGBoost model."""
    return model.predict(X)

def evaluate_model(y_true, y_pred):
    """Compute standard evaluation metrics for regression."""
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return {'mse': mse, 'rmse': rmse}

def compute_strategy_alpha(lagged_df, y_pred, benchmark_col='close'):
    """
    Compute strategy alpha: predicted return vs. actual.
    Adds predicted returns and alpha to the lagged_df and returns result + mean alpha.
    """
    result = lagged_df.copy()
    result['predicted_close'] = y_pred
    result['strategy_return'] = result['predicted_close'].pct_change()
    result['benchmark_return'] = result[benchmark_col].pct_change()
    result['alpha'] = result['strategy_return'] - result['benchmark_return']
    mean_alpha = result['alpha'].mean()
    return result, mean_alpha

def plot_feature_importance(model, feature_names):
    """Display a bar chart of XGBoost feature importance."""
    xgb.plot_importance(model, importance_type='weight', xlabel='F Score', ylabel='Features')
    plt.title("XGBoost Feature Importance")
    plt.tight_layout()
    plt.show()

# Example pipeline usage:
# (This will be placed in a notebook or main application file, not in the module)
if __name__ == "__main__":
    # Assume dataframe df exists with OHLCV columns and 'timestamp'
    # df = pd.read_csv('your_data.csv')

    # Step 1: Prepare data (user should provide df)
    # features, targets, lagged_df = prepare_features_targets(df, target_col='close', lags=5)
    # X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, shuffle=False)

    # Step 2: Train model
    # model = train_xgboost(X_train, y_train)

    # Step 3: Predict
    # y_pred = predict_xgboost(model, X_test)

    # Step 4: Evaluate
    # metrics = evaluate_model(y_test, y_pred)
    # print(metrics)

    # Step 5: Compute alpha
    # lagged_test = lagged_df.iloc[X_test.index]
    # strategy_result, mean_alpha = compute_strategy_alpha(lagged_test, y_pred, benchmark_col='close')
    # print("Mean Strategy Alpha:", mean_alpha)

    # Step 6: Feature importance
    # plot_feature_importance(model, X_train.columns)
    pass

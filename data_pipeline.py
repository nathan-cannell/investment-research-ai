import requests
from polygon import RESTClient
import pandas as pd

def OHLCV(API_KEY, ticker, from_date, to_date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}?apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    bars = []
    for bar in data.get("results", []):
        bars.append({
            "timestamp": bar["t"],
            "open": bar["o"],
            "high": bar["h"],
            "low": bar["l"],
            "close": bar["c"],
            "volume": bar["v"]
        })
    df = pd.DataFrame(bars)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


def base_returns(API_KEY, ticker, from_date, to_date):
    client = RESTClient(API_KEY)
    aggs = []
    for a in client.list_aggs(
        ticker,     # S&P 500 index ticker
        1,           # 1-day bars
        "day",
        from_date, # Start date
        to_date, # End date
        limit=50000
    ):
        aggs.append(a)
        # Convert to DataFrame
    data = [{
        'timestamp': a.timestamp,
        'open': a.open,
        'high': a.high,
        'low': a.low,
        'close': a.close,
        'volume': a.volume,
        'vwap': a.vwap,
        'transactions': a.transactions
    } for a in aggs]
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)


    # Assuming you have a DataFrame 'spy_df' with 'date' and 'close' columns
    df['return'] = df['close'].pct_change()
    
    # Resample to quarterly and calculate compounded return
    df_quarterly = (1 + df['return']).resample('Q').prod() - 1
    df_quarterly = df_quarterly.rename('spy_quarterly_return')
    return df, df_quarterly

def future_excess_return(portfolio_return, benchmark_return):
    excess_return = portfolio_return - benchmark_return
    return excess_return

def main():
    print("Data Pipeline Initialized")
    API_KEY = "TTXLaHBArYCOrGJpkuNaMJdVeJ0dLDRG"
    from_date = "2025-01-01"
    to_date = "2025-07-10"

    # excess_return = future_excess_return(0.10, 0.03)
    apple_vals = OHLCV(API_KEY, "AAPL", from_date, to_date)
    bench_returns, spy_quarterly = base_returns(API_KEY, "SPY", from_date, to_date)



    print(apple_vals.head())
    print(bench_returns.head())
    print(spy_quarterly.head())


if __name__ == "__main__":
    main()

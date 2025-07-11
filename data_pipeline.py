import requests
from polygon import RESTClient

def OHLCV(API_KEY, ticker, from_date, to_date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}?apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    for bar in data.get("results", []):
        print({
            "date": bar["t"],
            "open": bar["o"],
            "high": bar["h"],
            "low": bar["l"],
            "close": bar["c"],
            "volume": bar["v"]
        })

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
    return aggs

def future_excess_return(portfolio_return, benchmark_return):
    excess_return = portfolio_return - benchmark_return
    return excess_return

def main():
    print("Data Pipeline Initialized")
    API_KEY = "TTXLaHBArYCOrGJpkuNaMJdVeJ0dLDRG"
    ticker = "AAPL"
    from_date = "2025-01-01"
    to_date = "2025-07-10"

    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}?apiKey={API_KEY}"

    excess_return = future_excess_return(0.10, 0.03)
    OHLCV(API_KEY, ticker, from_date, to_date)
    bench_returns = base_returns(API_KEY, "I:SPX", from_date, to_date)
    print(bench_returns)
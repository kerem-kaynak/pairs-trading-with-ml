from typing import Optional, List, Dict, Tuple
from dotenv import load_dotenv
import requests
import os
import pandas as pd

load_dotenv()

POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY")


def get_all_etf_tickers() -> List[Dict[str, str]]:
    req_url = f"https://api.polygon.io/v3/reference/tickers?type=ETF&market=stocks&exchange=XNAS&active=true&?date=2023-01-01&limit=1000&apiKey={POLYGON_API_KEY}"
    response = requests.get(req_url)
    if response.status_code == 200:
        tickers = [etf["ticker"] for etf in response.json()["results"]]
        return tickers
    else:
        print(
            f"Failed to get ETF tickers\nStatus code: {response.status_code}\nResponse: {response.text}"
        )
        return None


def get_price_series(
    ticker: str, start_date: str, end_date: str
) -> Optional[List[Dict[str, float]]]:
    req_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey={POLYGON_API_KEY}"

    response = requests.get(req_url)
    if (response.status_code == 200) & ("results" in response.json()):
        return response.json()["results"]
    else:
        print(
            f"Failed to get price data for {ticker} from {start_date} to {end_date}\nStatus code: {response.status_code}\nResponse: {response.text}"
        )
        return None


def parse_timeseries(
    api_response: List[Dict[str, float]]
) -> Tuple[List[float], List[float]]:
    timestamps = []
    prices = []
    for data_point in api_response:
        timestamps.append(data_point["t"])
        prices.append(data_point["c"])
    return timestamps, prices


def create_etf_dataframe(
    ticker: str, timestamps: List[float], prices: List[float]
) -> pd.DataFrame:
    df = pd.DataFrame({"Timestamp": timestamps, ticker: prices})
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms", utc=True)
    df.set_index("Timestamp", inplace=True)
    return df


def filter_trading_days(df):
    df = df[df.index.weekday < 5]
    return df


etf_list = list(set(get_all_etf_tickers()))
start_date = "2018-01-01"
end_date = "2023-01-01"

dfs = []
rate = 1
for etf_symbol in etf_list:
    print(f"Processing: {etf_symbol}\nStatus: {rate}/{len(etf_list)}")
    price_series = get_price_series(etf_symbol, start_date, end_date)
    if price_series:
        timestamps, closing_prices = parse_timeseries(price_series)
        df = create_etf_dataframe(etf_symbol, timestamps, closing_prices)
        dfs.append(df)
    # if rate % 4 == 0:
    #     time.sleep(60)
    rate += 1

merged_df = pd.concat(dfs, axis=1)

merged_df = merged_df.sort_index(axis=1)

merged_filtered_df = filter_trading_days(merged_df)

merged_filtered_df.to_csv("../data/etf_prices.csv")

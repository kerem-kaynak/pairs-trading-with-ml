from typing import Optional, List, Dict, Tuple
from dotenv import load_dotenv
import requests
import os
import pandas as pd

load_dotenv()

POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY")


def get_all_tech_tickers() -> List[str]:
    tech_quotes = pd.read_csv("./data/nasdaq_stock_screener_tech_quotes.csv")
    nasdaq_tech_tickers = tech_quotes['Symbol'].tolist()
    return nasdaq_tech_tickers

def get_all_etf_tickers() -> List[str]:
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


def filter_trading_days(df: pd.DataFrame):
    df = df[df.index.weekday < 5]
    return df

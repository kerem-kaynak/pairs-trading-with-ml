from utils.price_series import get_all_etf_tickers, get_price_series, parse_timeseries, create_etf_dataframe, filter_trading_days
import pandas as pd

stock_list = list(set(get_all_etf_tickers()))
start_date = "2018-01-01"
end_date = "2023-01-01"

dfs = []
rate = 1
for stock_symbol in stock_list:
    print(f"Processing: {stock_symbol}\nStatus: {rate}/{len(stock_list)}")
    price_series = get_price_series(stock_symbol, start_date, end_date)
    if price_series:
        timestamps, closing_prices = parse_timeseries(price_series)
        df = create_etf_dataframe(stock_symbol, timestamps, closing_prices)
        dfs.append(df)
    rate += 1

merged_df = pd.concat(dfs, axis=1)

merged_df = merged_df.sort_index(axis=1)

merged_filtered_df = filter_trading_days(merged_df)

merged_filtered_df.to_csv("./data/etf_prices.csv")
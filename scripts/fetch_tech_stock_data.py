from utils.price_series import get_all_tech_tickers, get_price_series, parse_timeseries, create_etf_dataframe, filter_trading_days
import pandas as pd

etf_list = list(set(get_all_tech_tickers()))
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
    rate += 1

merged_df = pd.concat(dfs, axis=1)

merged_df = merged_df.sort_index(axis=1)

merged_filtered_df = filter_trading_days(merged_df)

merged_filtered_df.to_csv("./data/tech_stock_prices.csv")
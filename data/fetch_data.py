import ccxt
import pandas as pd
import time

def fetch_data(symbol="BTC/USDT", timeframe="1h", start="2021-01-01", end="2024-01-01", limit=1000):
    exchange = ccxt.bybit()
    since, end_ts = int(pd.Timestamp(start).timestamp() * 1000), int(pd.Timestamp(end).timestamp() * 1000)
    all_data, total_fetched = [], 0

    while since < end_ts:
        try:
            data = exchange.fetch_ohlcv(symbol, timeframe, since, limit, params={"category": "spot"})
            if not data: break

            df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            if len(all_data) > 0 and df["timestamp"].iloc[-1] <= all_data[-1]["timestamp"].iloc[-1]: break

            all_data.append(df)
            total_fetched += len(df)
            since = int(df["timestamp"].iloc[-1].timestamp() * 1000)
            time.sleep(0.5)
        except Exception as e:
            print(e)
            break

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/btc_usdt_1h_2021_2023.csv", index=False)
        return final_df
    else:
        print("error")
        return None

if __name__ == "__main__":
    fetch_data()

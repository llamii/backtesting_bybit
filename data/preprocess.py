import pandas as pd
import ta

def preprocess_data(file_path="data/btc_usdt_1h_2021_2023.csv"):
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    df = df[~df.index.duplicated(keep="first")]
    df.dropna(inplace=True)

    df["ema_10"] = ta.trend.ema_indicator(df["close"], window=10)
    df["ema_50"] = ta.trend.ema_indicator(df["close"], window=50)
    df["rsi"] = ta.momentum.rsi(df["close"], window=14)
    df["atr"] = ta.volatility.average_true_range(df["high"], df["low"], df["close"], window=14)

    df.to_csv("data/btc_usdt_1h_2021_2023_processed.csv")
    return df

if __name__ == "__main__":
    preprocess_data()

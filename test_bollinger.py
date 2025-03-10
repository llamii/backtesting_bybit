import pandas as pd
import matplotlib.pyplot as plt
from backtesting.optimize_bollinger import backtest_bollinger_strategy

def compute_bollinger_bands(df, sma_window=30, bb_window=15, bb_std=1.5):
    df["sma"] = df["close"].rolling(window=sma_window).mean()
    df["bb_middle"] = df["close"].rolling(window=bb_window).mean()
    df["bb_upper"] = df["bb_middle"] + (df["close"].rolling(window=bb_window).std() * bb_std)
    df["bb_lower"] = df["bb_middle"] - (df["close"].rolling(window=bb_window).std() * bb_std)

def test_bollinger(file_path="data/btc_usdt_1h_2021_2023_processed.csv"):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])

    compute_bollinger_bands(df, sma_window=30, bb_window=15, bb_std=1.5)
    profit = backtest_bollinger_strategy(df.copy(), sma_window=30, bb_window=15, bb_std=1.5)

    print(f"Прибыль стратегии Bollinger Bands: {profit:.2f} USDT")

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["close"], label="Цена BTC/USDT", alpha=0.5)
    plt.plot(df["timestamp"], df["bb_upper"], label="Верхняя полоса", linestyle="--", color="r")
    plt.plot(df["timestamp"], df["bb_lower"], label="Нижняя полоса", linestyle="--", color="g")
    plt.legend()
    plt.xlabel("Дата")
    plt.ylabel("Цена (USDT)")
    plt.title("Bollinger Bands на 2024 году")
    plt.show()

if __name__ == "__main__":
    test_bollinger()

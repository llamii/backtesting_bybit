import pandas as pd
import numpy as np

def backtest_bollinger_strategy(df, sma_window, bb_window, bb_std, initial_balance=10000):
    df["sma"] = df["close"].rolling(window=sma_window).mean()
    df["bb_middle"] = df["close"].rolling(window=bb_window).mean()
    df["bb_upper"] = df["bb_middle"] + (df["close"].rolling(window=bb_window).std() * bb_std)
    df["bb_lower"] = df["bb_middle"] - (df["close"].rolling(window=bb_window).std() * bb_std)

    df["signal"] = 0
    df.loc[(df["close"] < df["bb_lower"]) & (df["close"] > df["sma"]), "signal"] = 1
    df.loc[(df["close"] > df["bb_upper"]) & (df["close"] < df["sma"]), "signal"] = -1
    df["signal"] = df["signal"].shift(1)

    balance, btc_balance = initial_balance, 0
    for i in range(1, len(df)):
        price, action = df.loc[df.index[i], "close"], df.loc[df.index[i], "signal"]
        if action == 1 and balance > 0:
            btc_balance, balance = balance / price, 0
        elif action == -1 and btc_balance > 0:
            balance, btc_balance = btc_balance * price, 0

    return balance + (btc_balance * df["close"].iloc[-1]) - initial_balance

def optimize_bollinger(file_path="data/btc_usdt_1h_2021_2023_processed.csv"):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])

    results = []
    best_profit, best_params = -np.inf, None

    for sma in range(30, 60, 10):
        for bb_window in range(10, 30, 5):
            for bb_std in np.linspace(1.5, 3.0, 4):
                profit = backtest_bollinger_strategy(df.copy(), sma, bb_window, bb_std)
                results.append((sma, bb_window, bb_std, profit))

                if profit > best_profit:
                    best_profit, best_params = profit, (sma, bb_window, bb_std)

    return pd.DataFrame(results, columns=["SMA", "BB Window", "BB Std", "Profit"])

if __name__ == "__main__":
    optimize_bollinger().to_csv("results/bollinger_optimization_results.csv", index=False)

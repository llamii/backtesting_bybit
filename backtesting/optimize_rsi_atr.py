import pandas as pd
import numpy as np

def backtest_rsi_atr_strategy(df, rsi_buy, rsi_sell, atr_filter, initial_balance=10000):
    df["signal"] = 0
    df.loc[(df["rsi"] < rsi_buy) & (df["atr"] > atr_filter), "signal"] = 1
    df.loc[(df["rsi"] > rsi_sell) & (df["atr"] > atr_filter), "signal"] = -1
    df["signal"] = df["signal"].shift(1)

    balance, btc_balance = initial_balance, 0
    for i in range(1, len(df)):
        price, action = df.loc[df.index[i], "close"], df.loc[df.index[i], "signal"]
        if action == 1 and balance > 0:
            btc_balance, balance = balance / price, 0
        elif action == -1 and btc_balance > 0:
            balance, btc_balance = btc_balance * price, 0

    return balance + (btc_balance * df["close"].iloc[-1]) - initial_balance

def optimize_rsi_atr(file_path="data/btc_usdt_1h_2021_2023_processed.csv"):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])

    results = []
    best_profit, best_params = -np.inf, None

    for rsi_buy in range(20, 40, 5):
        for rsi_sell in range(60, 85, 5):
            for atr_filter in np.linspace(1.0, 10, 5):
                if rsi_buy >= rsi_sell:
                    continue

                profit = backtest_rsi_atr_strategy(df.copy(), rsi_buy, rsi_sell, atr_filter)
                results.append((rsi_buy, rsi_sell, atr_filter, profit))

                if profit > best_profit:
                    best_profit, best_params = profit, (rsi_buy, rsi_sell, atr_filter)

    return pd.DataFrame(results, columns=["RSI Buy", "RSI Sell", "ATR Filter", "Profit"])

if __name__ == "__main__":
    optimize_rsi_atr().to_csv("results/rsi_atr_optimization_results.csv", index=False)

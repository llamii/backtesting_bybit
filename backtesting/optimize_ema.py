import pandas as pd
import numpy as np

def backtest_ema_strategy(df, ema_short, ema_long, initial_balance=10000):
    df["ema_short"] = df["close"].ewm(span=ema_short, adjust=False).mean()
    df["ema_long"] = df["close"].ewm(span=ema_long, adjust=False).mean()
    df["signal"] = np.where(df["ema_short"] > df["ema_long"], 1, -1)
    df["signal"] = df["signal"].shift(1)

    balance, btc_balance = initial_balance, 0
    for i in range(1, len(df)):
        price, action = df.loc[df.index[i], "close"], df.loc[df.index[i], "signal"]
        if action == 1 and balance > 0:
            btc_balance, balance = balance / price, 0
        elif action == -1 and btc_balance > 0:
            balance, btc_balance = btc_balance * price, 0

    return balance + (btc_balance * df["close"].iloc[-1]) - initial_balance

def greedy_optimize_ema(file_path="data/btc_usdt_1h_2021_2023_processed.csv"):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])

    step_size = 5
    best_ema_short, best_ema_long = 10, 50
    best_profit = backtest_ema_strategy(df.copy(), best_ema_short, best_ema_long)

    results = []
    while True:
        candidates = [
            (best_ema_short + step_size, best_ema_long),
            (best_ema_short - step_size, best_ema_long),
            (best_ema_short, best_ema_long + step_size),
            (best_ema_short, best_ema_long - step_size)
        ]

        improving = False
        for ema_short, ema_long in candidates:
            if ema_short < 5 or ema_long < 20 or ema_short >= ema_long:
                continue

            profit = backtest_ema_strategy(df.copy(), ema_short, ema_long)
            results.append((ema_short, ema_long, profit))

            if profit > best_profit:
                best_profit, best_ema_short, best_ema_long = profit, ema_short, ema_long
                improving = True

        if not improving:
            break

    return pd.DataFrame(results, columns=["EMA Short", "EMA Long", "Profit"])

if __name__ == "__main__":
    greedy_optimize_ema().to_csv("results/ema_optimization_results.csv", index=False)

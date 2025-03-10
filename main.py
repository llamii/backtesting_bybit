import os
import pandas as pd
import matplotlib.pyplot as plt
from data.fetch_data import fetch_data
from data.preprocess import preprocess_data
from backtesting.optimize_ema import greedy_optimize_ema
from backtesting.optimize_rsi_atr import optimize_rsi_atr
from backtesting.optimize_bollinger import optimize_bollinger


def plot_results(results_file, strategy_name):
    df = pd.read_csv(results_file)
    plt.figure(figsize=(10, 5))
    plt.plot(df["Profit"], marker="o")
    plt.xlabel("Параметры")
    plt.ylabel("Прибыль (USDT)")
    plt.title(f"Оптимизация {strategy_name}")
    plt.show()

if __name__ == "__main__":
    print("Загрузка данных...")
    fetch_data()

    print("Обработка данных...")
    preprocess_data()

    print("Оптимизация EMA...")
    ema_results = greedy_optimize_ema()
    ema_results.to_csv(f"results/ema_optimization_results.csv", index=False)
    plot_results(f"results/ema_optimization_results.csv", "EMA")

    print("Оптимизация RSI + ATR...")
    rsi_results = optimize_rsi_atr()
    rsi_results.to_csv(f"results/rsi_atr_optimization_results.csv", index=False)
    plot_results(f"results/rsi_atr_optimization_results.csv", "RSI + ATR")

    print("Оптимизация Bollinger Bands...")
    bollinger_results = optimize_bollinger()
    bollinger_results.to_csv(f"results/bollinger_optimization_results.csv", index=False)
    plot_results(f"results/bollinger_optimization_results.csv", "Bollinger Bands")

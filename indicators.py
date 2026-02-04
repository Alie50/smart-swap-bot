import pandas as pd
import numpy as np

# ===== EMA =====
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

# ===== RSI =====
def rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ===== MACD =====
def macd(series, fast=12, slow=26, signal=9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

# ===== Bollinger Bands =====
def bollinger_bands(series, period=20, std=2):
    middle = series.rolling(period).mean()
    std_dev = series.rolling(period).std()
    upper = middle + (std_dev * std)
    lower = middle - (std_dev * std)
    return upper, middle, lower

# ===== Volume Strength =====
def volume_strength(volume, period=20):
    avg_volume = volume.rolling(period).mean()
    return volume > avg_volume


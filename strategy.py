from indicators import ema, rsi, macd, bollinger_bands, volume_strength

# ===== BUY CONDITIONS =====
def should_buy(df, config):
    close = df["close"]
    volume = df["volume"]

    rsi_val = rsi(close).iloc[-1]
    upper, middle, lower = bollinger_bands(close)
    price = close.iloc[-1]

    vol_ok = volume_strength(volume).iloc[-1]

    # شروط الشراء الصارمة
    if (
        rsi_val <= config["buy"]["rsi_below"]
        and price <= lower.iloc[-1] * 1.01
        and vol_ok
    ):
        return True

    return False


# ===== SELL CONDITIONS =====
def should_sell(df, config):
    close = df["close"]
    volume = df["volume"]

    rsi_val = rsi(close).iloc[-1]
    upper, middle, lower = bollinger_bands(close)
    price = close.iloc[-1]

    vol_ok = volume_strength(volume).iloc[-1]

    # شروط البيع الصارمة
    if (
        rsi_val >= config["sell"]["rsi_above"]
        and price >= upper.iloc[-1] * 0.99
        and vol_ok
    ):
        return True

    return False


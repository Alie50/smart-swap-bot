from indicators import ema, rsi, bollinger_bands, volume_strength

# ===== BUY CONDITIONS =====
def should_buy(df, config):
    close = df["close"]
    volume = df["volume"]

    price = close.iloc[-1]
    rsi_val = rsi(close).iloc[-1]

    ema_fast = ema(close, config["ema_fast"]).iloc[-1]
    ema_trend = ema(close, config["ema_trend"]).iloc[-1]

    upper, middle, lower = bollinger_bands(close)
    vol_ok = volume_strength(volume).iloc[-1]

    # تفكير تحليلي: هبوط + انعكاس + أمان اتجاه
    if (
        rsi_val <= config["buy"]["rsi_below"]
        and price <= lower.iloc[-1] * 1.01
        and price > ema_fast            # بداية انعكاس
        and price > ema_trend           # لا نشتري في انهيار
        and vol_ok
    ):
        return True

    return False


# ===== SELL CONDITIONS =====
def should_sell(df, config):
    close = df["close"]
    volume = df["volume"]

    price = close.iloc[-1]
    rsi_val = rsi(close).iloc[-1]

    ema_fast = ema(close, config["ema_fast"]).iloc[-1]

    upper, middle, lower = bollinger_bands(close)
    vol_ok = volume_strength(volume).iloc[-1]

    # تفكير تحليلي: صعود ثم بداية هبوط
    if (
        rsi_val >= config["sell"]["rsi_above"]
        and price >= upper.iloc[-1] * 0.99
        and price < ema_fast            # كسر نزول = خروج
        and vol_ok
    ):
        return True

    return False

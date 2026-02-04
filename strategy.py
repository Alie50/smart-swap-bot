def should_buy(df, config):
    if len(df) < 30:
        return False

    close = df["close"]
    volume = df["volume"]

    rsi_val = rsi(close).iloc[-1]
    upper, middle, lower = bollinger_bands(close)
    price = close.iloc[-1]
    ema_200 = ema(close, 200).iloc[-1]

    vol_ok = volume_strength(volume).iloc[-1]

    if (
        rsi_val <= config["buy"]["rsi_below"]
        and price <= lower.iloc[-1] * 1.01
        and price > ema_200
        and vol_ok
    ):
        return True

    return False

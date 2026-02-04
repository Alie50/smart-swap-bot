import yaml
import pandas as pd

from strategy import should_buy, should_sell

# ===== Load Config =====
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

symbol = config["symbols"][0]
timeframe = config["timeframe"]

print(f"Running analysis for {symbol} on {timeframe}")

# ===== Dummy Market Data (Test Only) =====
data = {
    "close": [1, 1.01, 1.02, 1.01, 1.00, 0.99, 1.00, 1.01],
    "volume": [100, 120, 130, 110, 140, 160, 180, 200]
}

df = pd.DataFrame(data)

# ===== Decision =====
if should_buy(df, config):
    print("DECISION: BUY (Swap USDT → Coin)")

elif should_sell(df, config):
    print("DECISION: SELL (Swap Coin → USDT)")

else:
    print("DECISION: WAIT (No Action)")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yaml
import pandas as pd

from strategy import should_buy, should_sell

# ===== Config Helpers =====
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def save_config(config):
    with open("config.yaml", "w") as f:
        yaml.safe_dump(config, f)

# ===== Commands =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Smart Swap Bot\n\n"
        "الأوامر المتاحة:\n"
        "/status\n"
        "/symbol SHIBUSDT\n"
        "/percent 20\n"
        "/decision"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    symbols = ", ".join(config["symbols"])
    await update.message.reply_text(
        f"📊 الحالة الحالية:\n"
        f"العملات: {symbols}\n"
        f"النسبة: {config['use_percent']}%\n"
        f"الفريم: {config['timeframe']}"
    )

async def set_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ استخدم: /symbol SHIBUSDT")
        return

    symbol = context.args[0].upper()
    config = load_config()
    config["symbols"] = [symbol]
    save_config(config)

    await update.message.reply_text(f"✅ تم تعيين العملة: {symbol}")

async def set_percent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ استخدم: /percent 20")
        return

    percent = int(context.args[0])
    config = load_config()
    config["use_percent"] = percent
    save_config(config)

    await update.message.reply_text(f"✅ تم تعيين النسبة: {percent}%")

# ===== REAL DECISION (تحليل فعلي) =====
async def decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()

    # بيانات اختبار (مؤقتًا – لاحقًا نستبدلها ببيانات Binance)
    data = {
        "close": [1, 1.01, 1.02, 1.01, 1.00, 0.99, 1.00, 1.02],
        "volume": [100, 120, 130, 110, 140, 160, 180, 200]
    }
    df = pd.DataFrame(data)

    if should_buy(df, config):
        msg = (
            "🟢 القرار: BUY\n"
            "السبب:\n"
            "- هبوط سابق\n"
            "- انعكاس فوق EMA\n"
            "- RSI تشبع بيع\n"
            "- حجم تداول داعم"
        )

    elif should_sell(df, config):
        msg = (
            "🔴 القرار: SELL\n"
            "السبب:\n"
            "- صعود سابق\n"
            "- كسر EMA_fast نزولًا\n"
            "- RSI تشبع شراء\n"
            "- بداية هبوط مؤكدة"
        )

    else:
        msg = (
            "🟡 القرار: WAIT\n"
            "السبب:\n"
            "- لا يوجد انعكاس واضح\n"
            "- الاتجاه غير مكتمل"
        )

    await update.message.reply_text(msg)

# ===== Run Bot =====
def run_telegram_bot(token):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("symbol", set_symbol))
    app.add_handler(CommandHandler("percent", set_percent))
    app.add_handler(CommandHandler("decision", decision))

    app.run_polling()

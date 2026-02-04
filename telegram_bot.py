from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yaml

# ===== Load Config =====
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def save_config(config):
    with open("config.yaml", "w") as f:
        yaml.safe_dump(config, f)

# ===== Commands =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Smart Swap Bot جاهز\n"
        "الأوامر:\n"
        "/status\n"
        "/symbol\n"
        "/percent\n"
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
        await update.message.reply_text("استخدم: /symbol SHIBUSDT")
        return

    symbol = context.args[0].upper()
    config = load_config()
    config["symbols"] = [symbol]
    save_config(config)

    await update.message.reply_text(f"✅ تم تعيين العملة: {symbol}")

async def set_percent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /percent 20")
        return

    percent = int(context.args[0])
    config = load_config()
    config["use_percent"] = percent
    save_config(config)

    await update.message.reply_text(f"✅ تم تعيين النسبة: {percent}%")

async def decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 آخر قرار:\n"
        "راجع bot.py (سيتم ربطه بالقرار الفعلي لاحقًا)"
    )

# ===== Main =====
def run_telegram_bot(token):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("symbol", set_symbol))
    app.add_handler(CommandHandler("percent", set_percent))
    app.add_handler(CommandHandler("decision", decision))

    app.run_polling()


import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError(
"BOT_TOKEN environment variable is not set. "
"Set BOT_TOKEN before running the bot."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛏️ MineBot - Mining Fleet Calculator\n\n"
        "Available Commands:\n\n"

        "📊 Fleet Matching Solver\n"
        "/fleet\n\n"

        "🚚 Hauler Cycle Time Solver\n"
        "/cycletimehauler\n\n"

        "Instructions:\n"
        "• Fill known values\n"
        "• Put ? on the value you want to calculate\n"
        "• Send the completed form back to MineBot"
    )

async def fleet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Fleet Matching Solver\n\n"
        "Fill known values and put ? for the unknown:\n\n"
        "Matching Factor =\n"
        "nHaulers =\n"
        "Loader Serving Time (min) =\n"
        "nLoader =\n"
        "Hauler Cycle Time (min) ="
    )

async def cycletimehauler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚚 Hauler Cycle Time Solver\n\n"
        "Fill known values and put ? for the unknown:\n\n"
        "Distance (km) =\n"
        "Empty Speed (km/min) =\n"
        "Load Speed (km/min) =\n"
        "EST (min) =\n"
        "LST (min) =\n"
        "Disposal Time (min) =\n"
        "Loading Time (min) =\n"
        "Cycle Time (min) ="
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("fleet", fleet))
app.add_handler(CommandHandler("cycletimehauler", cycletimehauler))

app.run_polling()


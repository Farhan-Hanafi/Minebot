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
        "⛏️ Mining Fleet Calculator\n\n"
        "Available Commands:\n\n"

        "📊 Matching Factor\n"
        "/mf <Haulers> <Loader Serving Time> <Loaders> <Hauler Cycle Time>\n"
        "Example:\n"
        "/mf 8 3.5 1 28\n\n"

        "🚛 Required Haulers\n"
        "/nhauler <Target MF> <Loaders> <Hauler Cycle Time> <Loader Serving Time>\n"
        "Example:\n"
        "/nhauler 1 1 28 3.5\n\n"

        "🚜 Required Loaders\n"
        "/nloader <Haulers> <Loader Serving Time> <Target MF> <Hauler Cycle Time>\n"
        "Example:\n"
        "/nloader 8 3.5 1 28\n\n"

        "⏱️ Loader Serving Time\n"
        "/stloader <Target MF> <Loaders> <Hauler Cycle Time> <Haulers>\n"
        "Example:\n"
        "/stloader 1 1 28 8\n\n"

        "🔄 Hauler Cycle Time\n"
        "/cthauler <Haulers> <Loader Serving Time> <Target MF> <Loaders>\n"
        "Example:\n"
        "/cthauler 8 3.5 1 1"
    )


async def mf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        h = float(context.args[0])
        st = float(context.args[1])
        l = float(context.args[2])
        ct = float(context.args[3])

        result = (h * st) / (l * ct)

        await update.message.reply_text(
            f"📊 Matching Factor = {result:.2f}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/mf <Haulers> <Loader Serving Time> <Loaders> <Hauler Cycle Time>\n\n"
            "Example:\n/mf 8 3.5 1 28"
        )


async def nhauler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mf_value = float(context.args[0])
        nloader = float(context.args[1])
        cthauler = float(context.args[2])
        stloader = float(context.args[3])

        result = (mf_value * nloader * cthauler) / stloader

        await update.message.reply_text(
            f"🚛 Required Haulers = {result:.2f}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/nhauler <Target MF> <Loaders> <Hauler Cycle Time> <Loader Serving Time>\n\n"
            "Example:\n/nhauler 1 1 28 3.5"
        )


async def nloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nhauler = float(context.args[0])
        stloader = float(context.args[1])
        mf_value = float(context.args[2])
        cthauler = float(context.args[3])

        result = (nhauler * stloader) / (mf_value * cthauler)

        await update.message.reply_text(
            f"🚜 Required Loaders = {result:.2f}"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/nloader <Haulers> <Loader Serving Time> <Target MF> <Hauler Cycle Time>\n\n"
            "Example:\n/nloader 8 3.5 1 28"
        )


async def stloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mf_value = float(context.args[0])
        nloader = float(context.args[1])
        cthauler = float(context.args[2])
        nhauler = float(context.args[3])

        result = (mf_value * nloader * cthauler) / nhauler

        await update.message.reply_text(
            f"⏱️ Loader Serving Time = {result:.2f} minutes"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/stloader <Target MF> <Loaders> <Hauler Cycle Time> <Haulers>\n\n"
            "Example:\n/stloader 1 1 28 8"
        )


async def cthauler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nhauler = float(context.args[0])
        stloader = float(context.args[1])
        mf_value = float(context.args[2])
        nloader = float(context.args[3])

        result = (nhauler * stloader) / (mf_value * nloader)

        await update.message.reply_text(
            f"🔄 Hauler Cycle Time = {result:.2f} minutes"
        )

    except:
        await update.message.reply_text(
            "Usage:\n/cthauler <Haulers> <Loader Serving Time> <Target MF> <Loaders>\n\n"
            "Example:\n/cthauler 8 3.5 1 1"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("mf", mf))
app.add_handler(CommandHandler("nhauler", nhauler))
app.add_handler(CommandHandler("nloader", nloader))
app.add_handler(CommandHandler("stloader", stloader))
app.add_handler(CommandHandler("cthauler", cthauler))

app.run_polling()


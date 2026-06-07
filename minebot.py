import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError(
"BOT_TOKEN environment variable is not set. "
"Set BOT_TOKEN before running the bot."
)

FLEET = 1
CYCLETIME = 2

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
    return FLEET

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
    return CYCLETIME


async def fleet_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        values = {}

        for line in text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()

        unknowns = [k for k, v in values.items() if v == "?"]

        if len(unknowns) != 1:
            await update.message.reply_text(
                "❌ Exactly one parameter must contain ?"
            )
            return FLEET

        unknown = unknowns[0]

        mf = values.get("Matching Factor")
        nhauler = values.get("nHaulers")
        st = values.get("Loader Serving Time (min)")
        nloader = values.get("nLoader")
        ct = values.get("Hauler Cycle Time (min)")

        if mf != "?":
            mf = float(mf)

        if nhauler != "?":
            nhauler = float(nhauler)

        if st != "?":
            st = float(st)

        if nloader != "?":
            nloader = float(nloader)

        if ct != "?":
            ct = float(ct)

        if unknown == "Matching Factor":
            result = (nhauler * st) / (nloader * ct)

        elif unknown == "nHaulers":
            result = (mf * nloader * ct) / st

        elif unknown == "Loader Serving Time (min)":
            result = (mf * nloader * ct) / nhauler

        elif unknown == "nLoader":
            result = (nhauler * st) / (mf * ct)

        elif unknown == "Hauler Cycle Time (min)":
            result = (nhauler * st) / (mf * nloader)

        await update.message.reply_text(
            f"📊 Fleet Result\n\n"
            f"{unknown} = {result:.2f}"
        )

        return ConversationHandler.END

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)}"
        )
        return FLEET

async def cycletime_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        values = {}

        for line in update.message.text.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()

        unknowns = [k for k, v in values.items() if v == "?"]

        if len(unknowns) != 1:
            await update.message.reply_text(
                "❌ Exactly one parameter must contain ?"
            )
            return CYCLETIME

        unknown = unknowns[0]

        d = values.get("Distance (km)")
        es = values.get("Empty Speed (km/min)")
        ls = values.get("Load Speed (km/min)")
        est = values.get("EST (min)")
        lst = values.get("LST (min)")
        disp = values.get("Disposal Time (min)")
        load = values.get("Loading Time (min)")
        ct = values.get("Cycle Time (min)")

        def conv(v):
            return None if v == "?" else float(v)

        d = conv(d)
        es = conv(es)
        ls = conv(ls)
        est = conv(est)
        lst = conv(lst)
        disp = conv(disp)
        load = conv(load)
        ct = conv(ct)

        if unknown == "Cycle Time (min)":
            result = (
                d / es +
                d / ls +
                est +
                lst +
                disp +
                load
            )

        elif unknown == "Loading Time (min)":
            result = (
                ct -
                d / es -
                d / ls -
                est -
                lst -
                disp
            )

        else:
            await update.message.reply_text(
                "❌ Solving this parameter is not implemented yet."
            )
            return CYCLETIME

        await update.message.reply_text(
            f"🚚 Hauler Cycle Time Result\n\n"
            f"{unknown} = {result:.2f}"
        )
        return ConversationHandler.END

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)}"
        )
        return CYCLETIME

app = Application.builder().token(TOKEN).build()

fleet_handler = ConversationHandler(
    entry_points=[CommandHandler("fleet", fleet)],
    states={
        FLEET: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                fleet_calculate
            )
        ]
    },
    fallbacks=[],
)

cycletime_handler = ConversationHandler(
    entry_points=[CommandHandler("cycletimehauler", cycletimehauler)],
    states={
        CYCLETIME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                cycletime_calculate
            )
        ]
    },
    fallbacks=[],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))

app.add_handler(fleet_handler)
app.add_handler(cycletime_handler)

app.run_polling()


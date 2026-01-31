import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# =========================
# 🔐 ТОКЕНИ
# =========================

BOT_TOKEN = "8513214069:AAEfG7ChMIq1whSNa0iZSqui0nbh2JaJF2Q"

# =====================
# 🤖 OPENAI CLIENT
# =====================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY не заданий у змінних середовища")

client = OpenAI(api_key=OPENAI_API_KEY)


# =========================
# 🧠 SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are I am Lafet — a digital clone of Andriy Muzichenko.

Role:
• Officer
• Creator
• Strategist
• Host

Personality:
• Calm
• Direct
• Ironic
• No bullshit

Language: Ukrainian

Rules:
• Think before speaking
• Challenge weak ideas
• Offer clear structure
• Speak like a human, not a bot
"""

STATE = {
    "mode": "EXPERT",
}

# =========================
# 🤖 HANDLERS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 I am Lafet активний.\n\n"
        "Режими:\n"
        "/mode expert\n"
        "/mode creator\n"
        "/mode host\n\n"
        "Просто пиши запит без команд."
    )


async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        STATE["mode"] = context.args[0].upper()
        await update.message.reply_text(f"🔁 Режим змінено: {STATE['mode']}")
    else:
        await update.message.reply_text("⚠️ Вкажи режим: /mode expert | creator | host")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"[MODE: {STATE['mode']}]\n{user_text}"}
            ]
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Помилка AI:\n{e}"

    await update.message.reply_text(reply)


# =========================
# 🚀 MAIN
# =========================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🧠 I am Lafet with AI ЗАПУЩЕНО")
    app.run_polling()


if __name__ == "__main__":
    main()

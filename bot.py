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

# ======================
# 🔐 TOKENS
# ======================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

# ======================
# 🧠 SYSTEM PROMPT
# ======================

SYSTEM_PROMPT = """
You are I AM LAFET — a digital clone of Andriy Muzichenko.

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
"""

# ======================
# 🤖 HANDLERS
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "EXPERT"
    await update.message.reply_text(
        "🧠 I AM LAFET активний.\n\n"
        "Режими:\n"
        "/mode expert\n"
        "/mode creator\n"
        "/mode host\n\n"
        "Пиши повідомлення без команд."
    )

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Вкажи режим: /mode expert | creator | host")
        return

    context.user_data["mode"] = context.args[0].upper()
    await update.message.reply_text(f"🔁 Режим змінено: {context.user_data['mode']}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    mode = context.user_data.get("mode", "EXPERT")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"[MODE: {mode}]\n{user_text}"},
            ],
        )
        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Помилка AI:\n{e}"

    await update.message.reply_text(reply)

# ======================
# 🚀 MAIN
# ======================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🧠 I AM LAFET ЗАПУЩЕНО")
    app.run_polling()

if __name__ == "__main__":
    main()

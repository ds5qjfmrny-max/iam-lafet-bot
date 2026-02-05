import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# ======================
# ENV
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=OPENAI_API_KEY)

# ======================
# SYSTEM PROMPT
# ======================
SYSTEM_PROMPT = """
You are I AM LAFET — a digital clone of Andriy.
Tone: direct, sharp, ironic.
Language: Ukrainian.
No bullshit. Think before answering.
"""

# ======================
# HANDLERS
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 I AM LAFET активний.\n\nПросто напиши повідомлення."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Помилка AI: {e}"

    await update.message.reply_text(reply)

# ======================
# MAIN
# ======================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 I AM LAFET запущений")
    app.run_polling()

if __name__ == "__main__":
    main()

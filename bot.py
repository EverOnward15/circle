from quart import Quart, request
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Quart(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your new bot.")

bot_app.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(await request.get_json(force=True), bot_app.bot)
    bot_app.process_update(update)
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

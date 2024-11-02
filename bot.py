from quart import Quart, request
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Quart(__name__)
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.initialize()  # Ensure initialization is done here

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your new bot.")

# Add the command handler to the bot application
bot_app.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        json_data = await request.get_json(force=True)
        update = Update.de_json(json_data, bot_app.bot)
        await bot_app.process_update(update)
        return "ok"
    except Exception as e:
        print(f"Error processing update: {e}")
        return "error", 500

@app.route("/")
async def home():
    return "Welcome to the Circle Bot!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

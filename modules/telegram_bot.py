from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from .imdb_api import IMDbAPI
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TelegramBot:
    def __init__(self, token: str, spelling_checker):
        self.token = token
        self.spelling_checker = spelling_checker
        self.imdb = IMDbAPI()
        self.app = ApplicationBuilder().token(self.token).build()

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hi! Send any text and I'll check spelling. If I find mistakes I'll suggest corrections and try IMDB search.")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Send me messages. I reply when spelling seems wrong and show possible IMDB matches for the message.")

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text or ""
        miss = self.spelling_checker.check_spelling(text)

        if miss:
            corrections = {w: self.spelling_checker.correct_word(w) for w in miss}
            parts = ["Spelling errors found:"]
            for w, c in corrections.items():
                parts.append(f"- '{w}' -> '{c}'")
            # IMDb search on original whole text (optional)
            imdb_results = self.imdb.search(text)
            if imdb_results:
                parts.append("\nIMDb results:")
                for r in imdb_results:
                    parts.append(f"- {r.get('Title')} ({r.get('Year')})")
            else:
                parts.append("\nNo IMDb matches found or OMDb API key missing.")
            await update.message.reply_text("\n".join(parts))
        else:
            await update.message.reply_text("No obvious spelling errors detected.")

    async def run(self):
        await self.app.run_polling()

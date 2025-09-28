import os
import asyncio
from dotenv import load_dotenv
from modules.telegram_bot import TelegramBot
from modules.spelling_checker import SpellingChecker

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise SystemExit("Missing TELEGRAM_BOT_TOKEN in environment")

async def main():
    spelling_checker = SpellingChecker()
    bot = TelegramBot(TELEGRAM_BOT_TOKEN, spelling_checker)
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())

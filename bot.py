import asyncio
import os
from dotenv import load_dotenv
import telegram

load_dotenv()


async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    bot = telegram.Bot(token)
    async with bot:
        print(await bot.get_me())

if __name__ == '__main__':
    asyncio.run(main())

import asyncio
import os
from dotenv import load_dotenv
import telegram
from fetch_nasa_apod_images import download_nasa_apod_images


async def send_image(bot, chat_id, image_path):
    with open(image_path, 'rb') as f:
        await bot.send_photo(chat_id=chat_id, photo=f)


async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    bot = telegram.Bot(token)
    async with bot:
        updates = await bot.get_updates()
        if updates:
            updates = updates[0]
            print(updates)

        api_key = os.getenv('NASA_API_TOKEN')
        if not api_key:
            raise ValueError("NASA_API_TOKEN environment variable not set")
        images_path = download_nasa_apod_images(api_key)

        for image_path in images_path:
            await send_image(bot, os.getenv('TELEGRAM_CHANNEL_ID'), image_path)

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
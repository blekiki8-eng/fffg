import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

WEB_URL = "https://YOUR-APP.up.railway.app"

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 Fish Cash", web_app=WebAppInfo(url=WEB_URL))]
    ],
    resize_keyboard=True
)

@dp.message(F.text == "/start")
async def start(message: Message):
    user_id = message.from_user.id

    ref_link = f"https://t.me/YOUR_BOT?start={user_id}"

    await message.answer(
        f"🐟 Fish Cash\n\n"
        f"ID: {user_id}\n"
        f"Реферальне посилання:\n{ref_link}",
        reply_markup=kb
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

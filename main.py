import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

accounts = [
    {"id": 1, "name": "GTA VIP Account", "seller_id": 123456789},
]

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Стартуємо!")]],
        resize_keyboard=True
    )
    await message.answer("Привіт!", reply_markup=kb)

@dp.message(F.text == "🚀 Стартуємо!")
async def role(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Покупець"), KeyboardButton(text="Продавець")]],
        resize_keyboard=True
    )
    await message.answer("Ким ви являєтесь?", reply_markup=kb)

@dp.message(F.text.in_(["Покупець", "Продавець"]))
async def game(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Ukraine GTA")]],
        resize_keyboard=True
    )
    await message.answer("Яку ігру більше любиш?", reply_markup=kb)

@dp.message(F.text == "Ukraine GTA")
async def accounts_list(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="GTA VIP Account", callback_data="acc_1")]
    ])
    await message.answer("🔥 Топ аккаунтів:", reply_markup=kb)

@dp.callback_query(F.data == "acc_1")
async def confirm(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Так", callback_data="buy")],
        [InlineKeyboardButton(text="Ні", callback_data="cancel")]
    ])
    await callback.message.answer("Ви хочете купити цей аккаунт?", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

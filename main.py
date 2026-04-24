import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ДАНІ (поки прості) ---
accounts = {
    "pubg": [
        {"name": "🔥 PUBG Conqueror Account"},
        {"name": "💎 PUBG Premium Account"}
    ]
}

users = {}  # тут буде профіль

# --- ГОЛОВНЕ МЕНЮ ---
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Мій профіль"), KeyboardButton(text="📋 Список аккаунтів")],
            [KeyboardButton(text="🎮 Ігри для продажі аккаунтів")]
        ],
        resize_keyboard=True
    )

# --- СТАРТ ---
@dp.message(F.text == "/start")
async def start(message: Message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {"rating": 5, "sold": 0}

    await message.answer("Привіт 👋", reply_markup=main_menu())

# =====================
# 👤 ПРОФІЛЬ
# =====================

@dp.message(F.text == "👤 Мій профіль")
async def profile(message: Message):
    user = users.get(message.from_user.id)

    text = f"""
👤 Ваш профіль:

⭐ Рейтинг: {user['rating']}
📦 Продано аккаунтів: {user['sold']}
"""
    await message.answer(text)

# =====================
# 📋 СПИСОК АККАУНТІВ
# =====================

@dp.message(F.text == "📋 Список аккаунтів")
async def accounts_menu(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ua online (скоро)")],
            [KeyboardButton(text="Pubg")],
            [KeyboardButton(text="Ukraine GTA (скоро)")],
        ],
        resize_keyboard=True
    )

    await message.answer("Оберіть гру:", reply_markup=kb)

# --- PUBG АККАУНТИ ---
@dp.message(F.text == "Pubg")
async def pubg_accounts(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    for i, acc in enumerate(accounts["pubg"]):
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=acc["name"],
                callback_data=f"view_{i}"
            )
        ])

    await message.answer("🔥 Список аккаунтів PUBG:", reply_markup=kb)

# --- ПЕРЕГЛЯД АККАУНТА ---
@dp.callback_query(F.data.startswith("view_"))
async def view_account(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    acc = accounts["pubg"][index]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купити", callback_data="buy")],
    ])

    await callback.message.answer(
        f"📦 {acc['name']}\n\nХочете купити?",
        reply_markup=kb
    )

# =====================
# 🎮 ІГРИ ДЛЯ ПРОДАЖУ
# =====================

@dp.message(F.text == "🎮 Ігри для продажі аккаунтів")
async def games_for_sell(message: Message):
    await message.answer(
        "🎮 Доступні ігри:\n\n"
        "• Ua Online\n"
        "• Ukraine GTA\n"
        "• Pubg\n\n"
        "Функція продажу вже частково є 😉"
    )

# =====================
# ▶️ ЗАПУСК
# =====================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

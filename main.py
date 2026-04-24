import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ДАНІ ---
accounts = {
    "pubg": [],   # пусто для тесту
    "gta": [],
    "ua": []
}

users = {}

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
            [KeyboardButton(text="Ua online")],
            [KeyboardButton(text="Pubg")],
            [KeyboardButton(text="Ukraine GTA")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Оберіть гру:", reply_markup=kb)

# --- PUBG ---
@dp.message(F.text == "Pubg")
async def pubg_accounts(message: Message):
    if not accounts["pubg"]:
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🚀 Продати аккаунт")],
                      [KeyboardButton(text="⬅️ Назад")]],
            resize_keyboard=True
        )

        await message.answer(
            "😔 На жаль немає аккаунтів в продажі,\nале ти можеш бути перший!",
            reply_markup=kb
        )
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[])

    for i, acc in enumerate(accounts["pubg"]):
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=acc["name"],
                callback_data=f"view_pubg_{i}"
            )
        ])

    await message.answer("🔥 Список аккаунтів PUBG:", reply_markup=kb)

# --- GTA ---
@dp.message(F.text == "Ukraine GTA")
async def gta_accounts(message: Message):
    await message.answer("⏳ Скоро буде доступно")

# --- UA ONLINE ---
@dp.message(F.text == "Ua online")
async def ua_accounts(message: Message):
    await message.answer("⏳ Скоро буде доступно")

# =====================
# 👀 ПЕРЕГЛЯД АККАУНТА
# =====================
@dp.callback_query(F.data.startswith("view_pubg_"))
async def view_account(callback: CallbackQuery):
    index = int(callback.data.split("_")[2])
    acc = accounts["pubg"][index]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Купити", callback_data="buy")],
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
        "🎮 Тут скоро буде можливість продавати аккаунти\n\n"
        "Поки що працює тільки PUBG 😉"
    )

# =====================
# 🚀 ПРОДАТИ АККАУНТ
# =====================
@dp.message(F.text == "🚀 Продати аккаунт")
async def sell_account(message: Message):
    # просто додаємо демо акаунт
    accounts["pubg"].append({
        "name": f"Аккаунт від {message.from_user.first_name}"
    })

    await message.answer("✅ Ваш аккаунт додано в продаж!")

# =====================
# 🔙 НАЗАД
# =====================
@dp.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer("Головне меню:", reply_markup=main_menu())

# =====================
# ▶️ ЗАПУСК
# =====================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

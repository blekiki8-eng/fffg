import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- СТАНИ ---
class SellState(StatesGroup):
    game = State()
    description = State()
    photos = State()
    confirm = State()

# --- ДАНІ ---
accounts = {
    "pubg": [],
    "gta": [],
    "ua": []
}

users = {}

# --- МЕНЮ ---
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

    await message.answer(
        f"👤 Профіль:\n⭐ {user['rating']}\n📦 Продано: {user['sold']}"
    )

# =====================
# 📋 СПИСОК
# =====================
@dp.message(F.text == "📋 Список аккаунтів")
async def accounts_menu(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Pubg")],
            [KeyboardButton(text="Ua online")],
            [KeyboardButton(text="Ukraine GTA")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Оберіть гру:", reply_markup=kb)

# =====================
# PUBG
# =====================
@dp.message(F.text == "Pubg")
async def pubg_accounts(message: Message):
    if not accounts["pubg"]:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🚀 Продати аккаунт")],
                [KeyboardButton(text="⬅️ Назад")]
            ],
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
                text=acc["description"],
                callback_data=f"view_{i}"
            )
        ])

    await message.answer("🔥 Список аккаунтів:", reply_markup=kb)

# =====================
# 🚀 ПРОДАЖ
# =====================
@dp.message(F.text == "🚀 Продати аккаунт")
async def sell_start(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Pubg")],
            [KeyboardButton(text="Ukraine GTA")],
            [KeyboardButton(text="Ua online")]
        ],
        resize_keyboard=True
    )

    await state.set_state(SellState.game)
    await message.answer("В якій грі продаєш аккаунт?", reply_markup=kb)

# --- ВИБІР ГРИ ---
@dp.message(SellState.game)
async def choose_game(message: Message, state: FSMContext):
    game_map = {
        "Pubg": "pubg",
        "Ukraine GTA": "gta",
        "Ua online": "ua"
    }

    game = game_map.get(message.text)
    if not game:
        return

    await state.update_data(game=game)
    await state.set_state(SellState.description)

    await message.answer("Опишіть ваш аккаунт:")

# --- ОПИС ---
@dp.message(SellState.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text, photos=[])
    await state.set_state(SellState.photos)

    await message.answer("Скиньте 3 фото аккаунта")

# --- ФОТО ---
@dp.message(SellState.photos)
async def photos(message: Message, state: FSMContext):
    if not message.photo:
        return

    data = await state.get_data()
    photos = data.get("photos", [])

    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)

    if len(photos) < 3:
        await message.answer(f"{len(photos)}/3 фото отримано")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Так", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="Ні", callback_data="confirm_no")]
    ])

    await state.set_state(SellState.confirm)

    await message.answer(
        "Перший раз безкоштовно, далі 20₴\n\nВиставити аккаунт?",
        reply_markup=kb
    )

# --- ПІДТВЕРДЖЕННЯ ---
@dp.callback_query(F.data == "confirm_no")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Скасовано ❌", reply_markup=main_menu())

@dp.callback_query(F.data == "confirm_yes")
async def confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    accounts[data["game"]].append({
        "description": data["description"]
    })

    await callback.message.answer("✅ Аккаунт виставлено!", reply_markup=main_menu())
    await state.clear()

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

import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- СТАНИ ---
class SellState(StatesGroup):
    choosing_game = State()
    description = State()
    photos = State()
    confirm = State()

# --- БАЗА (тимчасова) ---
accounts = {
    "gta": [],
    "pubg": [],
    "ua": []
}

# --- СТАРТ ---
@dp.message(F.text == "/start")
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Стартуємо!")]],
        resize_keyboard=True
    )
    await message.answer("Привіт 👋", reply_markup=kb)

# --- РОЛЬ ---
@dp.message(F.text == "🚀 Стартуємо!")
async def role(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Покупець"), KeyboardButton(text="Продавець")]],
        resize_keyboard=True
    )
    await message.answer("Ким ви являєтесь?", reply_markup=kb)

# =====================
# 🧑‍💼 ПРОДАВЕЦЬ
# =====================

@dp.message(F.text == "Продавець")
async def seller_start(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ua Online")],
            [KeyboardButton(text="Ukraine GTA")],
            [KeyboardButton(text="Pubg")]
        ],
        resize_keyboard=True
    )
    await state.set_state(SellState.choosing_game)
    await message.answer("В якій грі хочете продати аккаунт?", reply_markup=kb)

# --- ВИБІР ГРИ ---
@dp.message(SellState.choosing_game)
async def choose_game(message: Message, state: FSMContext):
    game_map = {
        "Ukraine GTA": "gta",
        "Pubg": "pubg",
        "Ua Online": "ua"
    }

    game = game_map.get(message.text)
    if not game:
        return

    await state.update_data(game=game)
    await state.set_state(SellState.description)

    await message.answer("Опишіть ваш аккаунт, що в ньому є:")

# --- ОПИС ---
@dp.message(SellState.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text, photos=[])
    await state.set_state(SellState.photos)

    await message.answer("Скиньте 3 фотки вашого аккаунта")

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
        await message.answer(f"Отримано {len(photos)}/3 фото")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Так", callback_data="sell_yes")],
        [InlineKeyboardButton(text="Ні", callback_data="sell_no")]
    ])

    await state.set_state(SellState.confirm)

    await message.answer(
        "Для першого разу безкоштовно.\nДалі 20₴\n\nВи хочете виставити аккаунт?",
        reply_markup=kb
    )

# --- ПІДТВЕРДЖЕННЯ ---
@dp.callback_query(F.data == "sell_no")
async def cancel_sell(callback, state: FSMContext):
    await state.clear()
    await callback.message.answer("Скасовано ❌ Напишіть /start")

@dp.callback_query(F.data == "sell_yes")
async def confirm_sell(callback, state: FSMContext):
    data = await state.get_data()

    game = data["game"]
    description = data["description"]

    accounts[game].append(description)

    await callback.message.answer("✅ Ваш аккаунт виставлено!")

    # показ списку
    text = "📋 Список аккаунтів:\n\n"
    for acc in accounts[game]:
        text += f"- {acc}\n"

    await callback.message.answer(text)

    await state.clear()

# =====================
# ▶️ ЗАПУСК
# =====================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

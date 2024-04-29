from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from keyboards.inline.start_keyboard import start__keybord
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!",reply_markup=start__keybord)


@dp.callback_query_handler(text='start')
async def start(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(f"Привет!",reply_markup=start__keybord)
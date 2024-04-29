from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram.types import CallbackQuery



@dp.callback_query_handler(text='food')
async def productt(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text(text='Раздел находится в разработке')
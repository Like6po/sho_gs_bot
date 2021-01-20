from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import GroupFilter
from loader import dp


@dp.message_handler(CommandStart(), GroupFilter())
async def bot_start(message: types.Message):
    await message.answer(f"Я работаю! Скинь войс!")

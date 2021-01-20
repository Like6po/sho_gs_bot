
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, ChatTypeFilter
from aiogram.types import ChatType

from loader import dp


@dp.message_handler(CommandStart(), ChatTypeFilter(ChatType.PRIVATE))
async def bot_start(message: types.Message):
    await message.answer('Ку привет! Добавь в чат и я буду переводить ваши войсы в текст!')
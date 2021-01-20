
import subprocess

import aiohttp

from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import ChatType, ContentType
from aiogram.utils.markdown import hbold

import os

from data.config import WIT_TOKEN
from loader import dp

# Windows
path = "C:\\Users\\Admin\\PycharmProjects\\crocodile_bot\\data\\voices\\"
pathffmpeg = "C:\\Users\\Admin\\Desktop\\ffmpeg\\bin\\"

# linux
#path = "data\\voices"
#pathffmpeg = ""

async def wit_speech(f):
    headers = {"authorization": f"Bearer {WIT_TOKEN}",
               'accept': 'application/vnd.wit.20200513+json',
               'Content-Type': 'audio/ogg'}
    url = "https://api.wit.ai/speech"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=f) as resp:
            info = await resp.json()
        return info


@dp.message_handler(ChatTypeFilter(ChatType.GROUP) | ChatTypeFilter(ChatType.SUPERGROUP),
                    content_types=ContentType.VOICE)
async def voice(message: types.Message):
    msg = await message.reply(f'{hbold("Обработка...")}')
    print(msg)
    code_name = f"{message.from_user.id}_{message.message_id}"

    await message.voice.download(f'{path}\\1_{code_name}.ogg')

    process = subprocess.run([f'{pathffmpeg}ffmpeg', '-i', f'{path}\\1_{code_name}.ogg',
                              f'{path}\\2_{code_name}.ogg'])
    if process.returncode != 0:
        return await msg.edit_text(f'{hbold("Не удалось распознать! (#1)")}')

    os.mkdir(f'{path}\\{code_name}')


    process = subprocess.run([f'{pathffmpeg}ffmpeg', '-i', f'{path}\\2_{code_name}.ogg',
                              '-f', 'segment', '-segment_time', '14', '-c', 'copy',
                              f'{path}\\{code_name}\\out_%03d.ogg'])
    if process.returncode != 0:
        return await msg.edit_text(f'{hbold("Не удалось распознать! (#2)")}')

    text = ''
    for file_name in os.listdir(f"{path}\\{code_name}"):

        resp = await wit_speech(open(f'{path}\\{code_name}\\{file_name}', 'rb'))
        try:
            os.remove(f'{path}\\{code_name}\\{file_name}')
        except:
            pass
        text += resp['text']

    await msg.edit_text(text=f"{message.from_user.get_mention()} сказал:\n{text}")

    try:
        os.remove(f'{path}2_{code_name}.ogg')
        os.remove(f'{path}1_{code_name}.ogg')
        os.rmdir(f"{path}\\{code_name}")
    except:
        pass

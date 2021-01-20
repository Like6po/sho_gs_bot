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


def win_pathes(code_name):
    path = "C:\\Users\\Admin\\PycharmProjects\\crocodile_bot\\data\\voices\\"
    pathffmpeg = "C:\\Users\\Admin\\Desktop\\ffmpeg\\bin\\"
    return {'path_1': f"{path}\\1_{code_name}.ogg",
            'path_2': f"{path}\\2_{code_name}.ogg",
            'path_ffmpeg': f"{pathffmpeg}ffmpeg",
            'path_dir': f'{path}\\{code_name}\\',
            'path_out': f'{path}\\{code_name}\\out_%03d.ogg'}


def linux_pathes(code_name):
    path = "./data/voices"
    pathffmpeg = ""
    return {'path_1': f"{path}/1_{code_name}.ogg",
            'path_2': f"{path}/2_{code_name}.ogg",
            'path_ffmpeg': f"{pathffmpeg}ffmpeg",
            'path_dir': f'{path}/{code_name}/',
            'path_out': f'{path}/{code_name}/out_%03d.ogg'}


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

    code_name = f"{message.from_user.id}_{message.message_id}"

    pathes = win_pathes(code_name)
    #pathes = linux_pathes(code_name)

    await message.voice.download(pathes['path_1'])

    process = subprocess.run([pathes['path_ffmpeg'], '-i', pathes['path_1'], pathes['path_2']],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if process.returncode != 0:
        return await msg.edit_text(f'{hbold("Не удалось распознать! (#1)")}')

    os.mkdir(pathes['path_dir'])

    process = subprocess.run([pathes['path_ffmpeg'], '-i', pathes['path_2'],
                              '-f', 'segment', '-segment_time', '14', '-c', 'copy',
                              pathes['path_out']], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if process.returncode != 0:
        return await msg.edit_text(f'{hbold("Не удалось распознать! (#2)")}')

    text = ''

    dir_list = os.listdir(pathes['path_dir'])
    dir_list.reverse()

    i = 0

    for file_name in dir_list:
        i += 1
        resp = await wit_speech(open(f"{pathes['path_dir']}{file_name}", 'rb'))
        try:
            os.remove(f"{pathes['path_dir']}{file_name}")
        except:
            pass
        print(resp)
        text = resp['text'] + " " + text
        if i < len(dir_list):
            await msg.edit_text(text=f"{message.from_user.get_mention()} сказал:\n{text}...")

    await msg.edit_text(text=f"{message.from_user.get_mention()} сказал:\n{text}")

    try:
        os.remove(pathes['path_1'])
        os.remove(pathes['path_2'])
        os.rmdir(pathes['path_dir'])
    except:
        pass

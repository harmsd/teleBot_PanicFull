import asyncio
import re
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from database.dao import get_all_panics

from keyboards.other_kb import get_cancel_kb, get_menu_kb
from keyboards.panic_kb import get_edit_db_kb
from bot import bot

def get_content_info(message: Message):
    content_type = None

    if message.photo:
        content_type = "photo"
    elif message.video:
        content_type = "video"
    elif message.document:
        content_type = "document"
    elif message.audio:
        content_type = "audio"
    elif message.text:
        content_type = "text"
    elif message.voice:
        content_type = "voice"
    
    content_text = message.text or message.caption
    return {'content_type': content_type, 'content_text': content_text}

async def send_message_user(bot, user_id, content_type, content_text=None, kb=None):
    match content_type:
        case 'text': await bot.send_message(chat_id=user_id, text=content_text, reply_markup=kb)
        case 'photo': await bot.send_message(chat_id=user_id, text=content_text, reply_markup=kb)
        case 'document': await bot.send_message(chat_id=user_id, text=content_text, reply_markup=kb)
        case 'video': await bot.send_message(chat_id=user_id, text=content_text, reply_markup=kb)
        case 'audio': await bot.send_message(chat_id=user_id, text=content_text, reply_markup=kb)
        case 'voice': await bot.send_message(chat_id=user_id, text=content_text, reply_markup=kb)

async def send_many_panic(all_panic, bot, user_id):
    for panic in all_panic:
        try: 
            content = Text(
                Bold("Название: "), panic.get("name"), "\n",
                Bold("Строчка panic: "), panic.get("panic_string"), "\n",
                Bold("Описание: "), panic.get("description"), "\n",
                Bold("Комментарии: "), panic.get("comment"), "\n"
            )
            await bot.send_message(chat_id=user_id, **content.as_kwargs(), reply_markup=get_edit_db_kb(panic.get("id")))

        except Exception as E:
            print(f'print; {E}')
            await asyncio.sleep(2)
        finally:
            await asyncio.sleep(0.5)
            
async def read_ips_file(message):
    def normalize_text(text):
        if text is None:
            return []
        return text.lower().replace(' ', '').replace('\n', '')
    
    try:
        await bot.download(
            message.document,
            destination=f"downloads/{message.document.file_id}.ips"
        )
        with open(f"downloads/{message.document.file_id}.ips", 'r') as downloaded_file:
            file_content_lines = downloaded_file.readlines()
        
        panicFull = {}
        for str in file_content_lines:
            new_str = str.replace('"', '')
            if('build' in new_str):
                content = new_str.split(":")
                string = content[1]
                num = string.find(',')
                panicFull["build"] = string[0:num]

            elif('product' in new_str):
                content = new_str.split(":")
                string = content[1]
                num = string.find(',')
                panicFull["product"] = string[0:num]

            elif('date' in new_str):
                content = new_str.split(":")
                string = content[1]
                panicFull["date"] = string[0:11]

            elif('panicString' in new_str):
                content = new_str.split(":")
                string = ''.join(content[1:6])
                panicFull['panicString'] = string
                panics = await get_all_panics(user_id=message.from_user.id)
                new_string = ''.join(content[1:])

                for panic in panics:    
                    name = panic.get('name')
                    if normalize_text(name) in normalize_text(new_string):
                        answer = panic.get("description")
                        break
                    else:
                        answer =f'К сожалению, поиск ключевого слова по нашей базе анализов не дал результата.\n' \
                                f'Мы обязательно добавим решение по данному анализу в ближайших обновлениях.' \
                                f'Если у вас есть другие panic-файлы, рекомендуем их также изучить и отправить нам, особенно если в них встречаются отличия.\n' \
                                f'Иногда полезная информация о сбое содержится только в одном из нескольких файлов.\n' 

        content = Text(
            Bold(f"Файл был выгружен: {panicFull.get('date')}\n"),
            Bold(f"Устройство: {panicFull.get('product')}\n"),
            Bold(f"Операционная система: {panicFull.get('build')}\n"),
            Bold(f"Panic String:\n{panicFull.get('panicString')}\n\n"),
            answer
        )

        await bot.send_message(chat_id=message.from_user.id, **content.as_kwargs(), reply_markup=get_cancel_kb())
        
    except Exception as E:
        print("Не получилось обработать файл!")
        print(f'print; {E}')
        answer_error = Text("Не получилоь обработать файл!")
        await bot.send_message(chat_id=message.from_user.id, **answer_error.as_kwargs(), reply_markup=get_menu_kb())
        await asyncio.sleep(2)
    finally:
        await asyncio.sleep(0.5)
        
        



from aiogram import Router, F
from aiogram.types import Message
from bot import bot
from aiogram.utils.formatting import (
    Bold, Text
)
from keyboards.for_db import get_db_kb
from keyboards.for_questions import get_yes_no_kb
from keyboards.for_cancel import get_cancel_kb

router = Router()

@router.message(F.document)
async def message_with_file(message: Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    panicFull = {}
    downloaded_file = await bot.download_file(file.file_path)
    file_content = downloaded_file.read().decode('utf-8')
    new_file_content = file_content.replace('"', "")
    file_content_lines = new_file_content.splitlines()
    for str in file_content_lines:
        new_str = str.replace(" ", "")
        if('build' in new_str):
            content = new_str.split(":")
            panicFull[content[0]] = content[1]
        elif('product' in new_str):
            content = new_str.split(":")
            panicFull[content[0]] = content[1]
        elif('date' in new_str):
            content = new_str.split(":")
            panicFull[content[0]] = content[1]
        elif('panicString' in new_str):
            content = new_str.split(":")
            panicFull[content[0]] = content[1:]
        
    content = Text(
        Bold(f"Файл был выгружен {panicFull.get('date')}"),
        Bold(f"\nУстройство: {panicFull.get('product')}"),
        Bold(f"\nОперационная система: {panicFull.get('build')}")
    )
    await message.answer(
        **content.as_kwargs()
    )

@router.message(F.text.lower() == "хочу редактировать бд")
async def message_with_edit_bd(message: Message):
    print(get_db_kb())
    content = Text(
        "Отлично, выбери операцию!"
    )
    await message.answer (
        **content.as_kwargs(),
        reply_markup=get_db_kb()
    )
    
@router.message(F.text)
async def message_with_text(message: Message):
    first_name = message.from_user.first_name
    content = Text(
            "Привет, ",
            Bold(first_name),
            "! Вы хотите получить информацию из файла PanicFull?🍏"
        )
    await message.answer(
        **content.as_kwargs(),
        reply_markup=get_yes_no_kb()
    )
from aiogram.utils.formatting import Text, Bold
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.for_questions import get_yes_no_kb
from keyboards.for_cancel import get_cancel_kb

router = Router()

@router.message(Command("start"))  
async def cmd_start(message: Message):
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

@router.callback_query(F.text.lower() == "информация из файла panicfull🍏")
async def answer_get_info(message: Message):
    await message.answer(
        "Хорошо, отправьте мне его ⬇️⬇️⬇️",
        reply_markup=get_cancel_kb()
    )

@router.message(F.text.lower() == "инструкция📖")
async def answer_get_instruction(message: Message):
    await message.answer(
        "Я больше ничего не умею...",
        reply_markup=get_cancel_kb()
    )

@router.message(F.text.lower() == "отмена")
async def answer_get_cancel(message: Message):
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

@router.message(F.sticker)
async def message_with_sticker(message: Message):
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

@router.message(F.animation)
async def message_with_animation(message: Message):
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
from aiogram.utils.formatting import Text, Bold, as_line
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.dao import set_user
from utils.utils import read_ips_file

from keyboards.other_kb import get_menu_kb, get_cancel_kb


router = Router()

@router.message(F.text == '🏠 Главное меню')
@router.message(Command("start"))   
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await set_user(tg_id=message.from_user.id, 
                          username=message.from_user.username,
                          full_name=message.from_user.full_name
                          )
    content = Text(
            "Привет, ",
            Bold(message.from_user.full_name),
            "! Вы хотите получить информацию из файла PanicFull?🍏"
    )
    if user is None:
        context = Text(
            "Привет, ",
            Bold(message.from_user.full_name),
            "! Вы хотите получить информацию из файла PanicFull?🍏"
        )
        
    await message.answer(
        **content.as_kwargs(),
        reply_markup=get_menu_kb()
    )

@router.message(F.text.lower() == "информация из файла panicfull🍏")
async def answer_get_info(message: Message):
    await message.answer(
        "Хорошо, отправьте мне его ⬇️⬇️⬇️",
        reply_markup=get_cancel_kb()
    )

@router.message(F.document)
async def handler_file(message: Message):
    await read_ips_file(message)

@router.message(F.text.lower() == "инструкция📖")
async def answer_get_instruction(message: Message):
    lines_content = as_line(
        Text(Bold("📥 Инструкция по отправке логов для анализа:\n")),
        Text(Bold("✅ Лучше всего отправлять:\n")),
        Text("• .ips файл (например, panic-full-data.ips)\n• .txt файл (например, экспортированный из 3uTools)\nЭто даст максимально точный результат и быстрый анализ!\n"),
        Text("⸻\n"),
        Text("Файлы можно отправлять прямо сюда, как с телефона, так и с компьютера.\n"),
        Text("⸻\n"),
        Text(Bold("🔍 Как найти panic-файл на iPhone:\n")),
        Text("1. Откройте Настройки\n2. Перейдите в Конфиденциальность и безопасность\n3. Выберите Аналитика и улучшения\n4. Перейдите в Данные аналитики\n5. Найдите файл, начинающийся с panic-full-...\nДля лучшего результата можно отправить несколько последних файлов.\n"),
        Text("⸻\n"),
    )
    await message.answer(
        **lines_content.as_kwargs(),
        reply_markup=get_cancel_kb()
    )

@router.message(F.text == "❌ Выйти")
async def answer_get_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Вы хотите получить информацию из файла PanicFull?🍏", reply_markup=get_menu_kb())
    
@router.message(F.text == "✅ Подтвердить")
async def answer_get_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Вы хотите получить информацию из файла PanicFull?🍏", reply_markup=get_menu_kb())
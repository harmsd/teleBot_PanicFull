import asyncio
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender
from bot import bot
from aiogram.utils.formatting import (
    Bold, Text
)
from keyboards.panic_kb import get_db_kb, add_panic_check
from keyboards.other_kb import get_menu_kb

from database.dao import add_panic, get_all_panics, delete_panic_by_id
from utils.utils import send_many_panic

class AddPanicStates(StatesGroup):
    name = State()
    panic_string = State()
    description = State()
    comment = State()
    check_state = State()


router = Router()

@router.message(F.text == "Редактирование БД")
async def message_with_edit_bd(message: Message, state: FSMContext):
    await state.clear()
    content = Text(
        "Отлично, ты в меню редактирование БД. Выбери операцию!"
    )
    await message.answer (
        **content.as_kwargs(),
        reply_markup=get_db_kb() 
    )

@router.callback_query(lambda c: c.data.startswith('delete_data_'))
async def process_callback_button(callback_query: types.CallbackQuery):
    try:
        panic_id = callback_query.data.split('_')[2]
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f'Удалены данные паника с id: {panic_id}!')
        await delete_panic_by_id(panic_id)
        await callback_query.message.delete()
    except Exception as e:
        await callback_query.answer("Ошибка при обрабтки", show_alert=True)
        print(f"Error in delete handler: {e}")

@router.message(F.text.lower() == "все panic")
async def all_view_panic(message: Message, state: FSMContext):
    await state.clear()
    all_panic = await get_all_panics(user_id=message.from_user.id)
    if all_panic:
        await send_many_panic(all_panic, bot, message.from_user.id)
        await message.answer(f'Все ваши {len(all_panic)} panic отправлены', reply_markup=get_db_kb())
    else:
        await message.answer('Пока нет ни одного panic!', reply_markup=get_menu_kb)
        
@router.message(F.text == "Добавить panic")
async def start_add_panic(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Напиши название panic", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddPanicStates.name)

@router.message(F.text, AddPanicStates.name)
async def add_panic_process(message: Message, state: FSMContext):
    await state.update_data(name=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Вставь необходимую строку с panic, чтобы я мог ее отличать от других")
    await state.set_state(AddPanicStates.panic_string)

@router.message(F.text, AddPanicStates.panic_string)
async def add_panic_process(message: Message, state: FSMContext):
    await state.update_data(panic_string=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Напиши описание этого panic, чтобы я мог его потом использовать в анализе файлов")
    await state.set_state(AddPanicStates.description)

@router.message(F.text, AddPanicStates.description)
async def add_panic_process(message: Message, state: FSMContext):
    await state.update_data(description=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Напиши комментарии какие-либо к этому panic. Они не будут использоваться в анализе файлов")
    await state.set_state(AddPanicStates.comment)
    
@router.message(F.text, AddPanicStates.comment)
async def add_panic_process(message: Message, state: FSMContext):
    await state.update_data(comment=message.text, user_id=message.from_user.id)
    data = await state.get_data()

    caption = f'Пожалуйста проверьте все ли верно: \n\n' \
              f'<b>Название panic: </b>{data.get("name")}\n' \
              f'<b>Строчка panic: </b>{data.get("panic_string")}\n' \
              f'<b>Описание: </b>{data.get("description")}\n' \
              f'<b>Комментари: </b>{data.get("comment")}\n'
    
    await message.answer(caption, reply_markup=add_panic_check())
    await state.set_state(AddPanicStates.check_state)

@router.message(AddPanicStates.check_state, F.text == '✅ Все верно')
async def confirm_add_note(message: Message, state: FSMContext):
    panic = await state.get_data()
    await add_panic(user_id=message.from_user.id, name=panic.get("name"), panic_string=panic.get("panic_string"), 
                    description=panic.get('description'), comment=panic.get('comment'))
    await message.answer('Panic успешно добавлен!', reply_markup=get_menu_kb())
    await state.clear()

@router.message(AddPanicStates.check_state, F.text == '❌ Отменить')
async def cancel_add_note(message: Message, state: FSMContext):
    await message.answer('Добавление panic отменено!', reply_markup=get_db_kb())
    await state.clear()
import asyncio
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender
from bot import bot

from database.dao import get_panic_by_id, update_description_panic, update_comment_panic, update_name_panic, update_panicString_panic

from keyboards.panic_kb import get_num_kb, get_db_kb

class EditPanicStates(StatesGroup):
    id = State()
    name = State()
    panic_string = State()
    description = State()
    comment = State()

router = Router()

@router.callback_query(lambda c: c.data.startswith('edit_data_'))
async def start_procces_edit(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        panic_id = callback_query.data.split('_')[2]
        panic = await get_panic_by_id(panic_id)
        await bot.answer_callback_query(callback_query.id)
        content = "Какие данные нужно изменить?\n" \
                  f"1 - Название: {panic.get("name")}\n" \
                  f"2 - Строчка panic: {panic.get("panic_string")}\n" \
                  f"3 - Описание: {panic.get("description")}\n" \
                  f"4 - Комментарии: {panic.get("comment")}"
        await bot.send_message(callback_query.from_user.id, content, reply_markup=get_num_kb())
        await state.update_data(id=panic_id)
    
    except Exception as e:
        await callback_query.answer("Ошибка при обработке", show_alert=True)
        print(f"Error in edit handler: {e}")

@router.message(F.text == "1")
async def start_edit_panic(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Напиши название panic", reply_markup=ReplyKeyboardRemove())

    await state.set_state(EditPanicStates.name)

@router.message(F.text, EditPanicStates.name)
async def start_edit_panic(message: Message, state: FSMContext):
    await state.update_data(name=message.text, user_id=message.from_user.id)
    panic = await state.get_data()
    await update_name_panic(panic.get('id'), panic.get('name'))
    await bot.send_message(chat_id=message.from_user.id, text=f"Данные обновлены! ✅", reply_markup=get_db_kb())

@router.message(F.text == "2")
async def start_edit_panic(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Напиши строчку panic", reply_markup=ReplyKeyboardRemove())
    await state.set_state(EditPanicStates.panic_string)

@router.message(F.text, EditPanicStates.panic_string)
async def start_edit_panic(message: Message, state: FSMContext):
    await state.update_data(panic_string=message.text, user_id=message.from_user.id)
    panic = await state.get_data()
    await update_panicString_panic(panic.get('id'), panic.get('panic_string'))
    await bot.send_message(message.from_user.id, text=f"Данные обновлены! ✅", reply_markup=get_db_kb())

@router.message(F.text == "3")
async def start_edit_panic(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Напиши описание panic", reply_markup=ReplyKeyboardRemove())
    await state.set_state(EditPanicStates.description)

@router.message(F.text, EditPanicStates.description)
async def start_edit_panic(message: Message, state: FSMContext):
    await state.update_data(description=message.text, user_id=message.from_user.id)
    panic = await state.get_data()
    await update_description_panic(panic.get('id'), panic.get('description'))
    await bot.send_message(message.from_user.id, text=f"Данные обновлены! ✅", reply_markup=get_db_kb())

@router.message(F.text == "4")
async def start_edit_panic(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer("Напиши комментарии к panic", reply_markup=ReplyKeyboardRemove())
    await state.set_state(EditPanicStates.comment)

@router.message(F.text, EditPanicStates.comment)
async def start_edit_panic(message: Message, state: FSMContext):
    await state.update_data(comment=message.text, user_id=message.from_user.id)
    panic = await state.get_data()
    await update_comment_panic(panic.get('id'), panic.get('comment'))
    await bot.send_message(message.from_user.id, text=f"Данные обновлены! ✅", reply_markup=get_db_kb())


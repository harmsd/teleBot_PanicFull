from aiogram.types import KeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_panic_check():
    kb_list = [
        [KeyboardButton(text="✅ Все верно"), KeyboardButton(text="❌ Отменить")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )

def get_db_kb():
    kb_list = [
        [KeyboardButton(text="Добавить panic"), KeyboardButton(text="Все panic"), KeyboardButton(text="❌ Выйти")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )

def get_edit_db_kb(panic_id: int):
    buttons = [
        [
            InlineKeyboardButton(text="Изменить", callback_data=f"edit_data_{panic_id}"),
            InlineKeyboardButton(text="Удалить", callback_data=f"delete_data_{panic_id}")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_num_kb():
    buttons = [
        [
        KeyboardButton(text="✅ Подтвердить"), KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3"), 
        KeyboardButton(text="4"), KeyboardButton(text="❌ Выйти")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )



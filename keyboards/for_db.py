from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_db_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить Panic', callback_data='add_pani')
    builder.button(text='Удалить Panic', callback_data='delete_panic')
    builder.button(text='Изменить Panic', callback_data='edit_panic')
    builder.button(text='Просмотреть всю таблицу паников', callback_data='show_panic')
    builder.adjust(3)
    
    return builder.as_markup(resize_keyboard=True)
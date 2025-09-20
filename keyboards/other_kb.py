from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Инструкция📖",)
    kb.button(text="Информация из файла PanicFull🍏")
    kb.button(text="Редактирование БД")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Выйти")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def kb_offer_post() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="📨 Предложить пост")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=False)
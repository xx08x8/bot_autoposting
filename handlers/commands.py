from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from func.all_func import *


router = Router()

@router.message(Command("ban"), F.from_user.id == ADMIN_ID)
async def ban_handler(message: Message):
    try:
        user_id = int(message.text.split(" ")[1])
        block_user(user_id)
        await message.answer(f"Пользователь с ID <code>{user_id}</code> был заблокирован.")
    except (IndexError, ValueError):
        await message.answer("Неверный формат команды. Используйте: /ban [user_id]")


@router.message(Command("unban"), F.from_user.id == ADMIN_ID)
async def unban_handler(message: Message):
    try:
        user_id = int(message.text.split(" ")[1])
        unblock_user(user_id)
        await message.answer(f"Пользователь с ID <code>{user_id}</code> был разблокирован.")
    except (IndexError, ValueError):
        await message.answer("Неверный формат команды. Используйте: /unban [user_id]")


@router.message(Command("blocked"), F.from_user.id == ADMIN_ID)
async def blocked_handler(message: Message):
    blocked_users = load_posts(BLOCKED_USERS_FILE)
    if blocked_users:
        blocked_list = "\n".join([f"<code>{user_id}</code>" for user_id in blocked_users])
        await message.answer(f"<b>Список заблокированных пользователей:</b>\n{blocked_list}")
    else:
        await message.answer("Список заблокированных пользователей пуст.")
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from typing import Optional
from func.all_func import *
from config.config import PENDING_POSTS_FILE, POSTS_PER_PAGE
from config.messages_list import NO_ACCESS
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    FSInputFile
)


bot: Bot

def set_bot(bot_instance):
    global bot
    bot = bot_instance

router = Router()

@router.message(F.text == "admin", F.from_user.id == ADMIN_ID)
async def admin_menu_handler(message: Message, state: FSMContext):
    if message.text.lower() =="admin":
        await show_posts(message, state, 0, message_id=None)
    else:
       await message.answer(NO_ACCESS)


async def show_posts(message: Message, state: FSMContext, page: int, message_id: Optional[int]):
    pending_posts =  await load_posts(PENDING_POSTS_FILE)
    total_posts = len(pending_posts)
    
    if not pending_posts:
        if message_id:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="Нет ожидающих постов.", reply_markup=None)
        else:
           await message.answer("Нет ожидающих постов.")
        return

    start_index = page * POSTS_PER_PAGE
    end_index = start_index + POSTS_PER_PAGE
    current_posts = pending_posts[start_index:end_index]

    navigation_buttons = []
    if page > 0:
       navigation_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"prev_page_{page - 1}"))
    if end_index < total_posts:
        navigation_buttons.append(InlineKeyboardButton(text="Вперед", callback_data=f"next_page_{page + 1}"))

    if not current_posts:
        if message_id:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="Нет ожидающих постов.", reply_markup=None)
        return

    post = current_posts[0]
    user_id = post["user_id"]
    file_path = post.get("image")
    text = post.get("text")
    
    approve_reject_buttons = [
                    InlineKeyboardButton(text="Подтвердить", callback_data=f"approve_{start_index}"),
                    InlineKeyboardButton(text="Отклонить", callback_data=f"reject_{start_index}"),
                ]
    
    keyboard = InlineKeyboardMarkup(
           inline_keyboard=[
               navigation_buttons,
                approve_reject_buttons,
            ]
        )
    
    caption = f"Новый пост от {user_id}\n\n"
    if text:
      caption += f"{text}\n\n"
    caption +=  f"Страница: {page + 1}/{((total_posts - 1) // POSTS_PER_PAGE) + 1}"


    if message_id:
        data = await state.get_data()
        old_message_id = data.get("message_id")
        old_page = data.get("page")

        if old_message_id == message_id and old_page == page:
            await state.update_data(page=page)
            return
        
    if file_path:
        if message_id:
          await bot.edit_message_media(
                 chat_id=message.chat.id,
                 message_id=message_id,
                 media=FSInputFile(file_path),
          )
          await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message_id,
                caption=caption,
                reply_markup=keyboard,
            )
        else:
          sent_message = await bot.send_photo(
                message.chat.id,
                photo=FSInputFile(file_path),
                caption=caption,
                reply_markup=keyboard,
            )
          message_id = sent_message.message_id

    elif text:
        if message_id:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text=caption,
                reply_markup=keyboard,
            )
        else:
           sent_message =  await bot.send_message(
                message.chat.id,
                text=caption,
                reply_markup=keyboard
            )
           message_id = sent_message.message_id
    else:
        if message_id:
          await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text=caption,
                reply_markup=keyboard,
            )
        else:
          sent_message =  await bot.send_message(
                message.chat.id,
                text=caption,
                reply_markup=keyboard,
            )
          message_id = sent_message.message_id
    await state.set_state("waiting_admin_decision")
    await state.update_data(message_id=message_id, page=page)
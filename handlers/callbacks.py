from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from func.all_func import *
from handlers.admin import show_posts
from config.config import PENDING_POSTS_FILE, POSTS_FILE, CHANNEL_ID
from config.messages_list import APPROVE, REJECTED, DONE, UNDONE, NOT_FOUND
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
)

bot: Bot

def set_bot(bot_instance):
    global bot
    bot = bot_instance

router = Router()

@router.callback_query(F.data.startswith("prev_page_"))
async def prev_page_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split("_")[-1])
    data = await state.get_data()
    message_id = data.get("message_id")
    await show_posts(query.message, state, page, message_id)

@router.callback_query(F.data.startswith("next_page_"))
async def next_page_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split("_")[-1])
    data = await state.get_data()
    message_id = data.get("message_id")
    await show_posts(query.message, state, page, message_id)


@router.callback_query(F.data == "approve_temp")
async def admin_approve_temp_handler(query: CallbackQuery, state: FSMContext):
    posts = await load_posts(POSTS_FILE)
    pending_posts = await load_posts(PENDING_POSTS_FILE)
    
    user_id_str = None
    if query.message.caption:
        user_id_str = query.message.caption.split(" ")[3]
    elif query.message.text:
        user_id_str = query.message.text.split(" ")[3]
    else:
        await query.answer("Не удалось определить пользователя.")
        return

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        await query.answer("Неверный формат ID пользователя.")
        return

    post = next((p for p in pending_posts if p["user_id"] == user_id and p["status"] == "pending"), None)

    if post:
        post["admin_id"] = query.from_user.id
        post["status"] = "approved"
        
        if post.get("image") and post.get("text"):
            await bot.send_photo(CHANNEL_ID, photo=FSInputFile(post["image"]), caption=post["text"])
        elif post.get("image"):
            await bot.send_photo(CHANNEL_ID, photo=FSInputFile(post["image"]))
        elif post.get("text"):
            await bot.send_message(CHANNEL_ID, post["text"])
        
        await bot.send_message(post["user_id"], APPROVE)
        await query.answer(DONE)
    
        posts.append(post)
        await save_posts(posts, POSTS_FILE)
        pending_posts.remove(post)
        await save_posts(pending_posts, PENDING_POSTS_FILE)
        await query.message.edit_reply_markup(reply_markup=None)
        
    else:
       await query.answer(NOT_FOUND)


@router.callback_query(F.data == "reject_temp")
async def admin_reject_temp_handler(query: CallbackQuery, state: FSMContext):
    pending_posts = await load_posts(PENDING_POSTS_FILE)
    user_id_str = None

    if query.message.caption:
        user_id_str = query.message.caption.split(" ")[3]
    elif query.message.text:
        user_id_str = query.message.text.split(" ")[3]
    else:
        await query.answer("Не удалось определить пользователя.")
        return

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        await query.answer("Неверный формат ID пользователя.")
        return
    
    post = next((p for p in pending_posts if p["user_id"] == user_id and p["status"] == "pending"), None)

    if post:
        post["admin_id"] = query.from_user.id
        post["status"] = "rejected"
        await bot.send_message(post["user_id"], REJECTED)
        await query.answer(UNDONE)
    
        pending_posts.remove(post)
        await save_posts(pending_posts, PENDING_POSTS_FILE)
        await query.message.edit_reply_markup(reply_markup=None)
    else:
       await query.answer(NOT_FOUND)
       

@router.callback_query(F.data.startswith("approve_"))
async def admin_approve_handler(query: CallbackQuery, state: FSMContext):
    posts = await load_posts(POSTS_FILE)
    pending_posts = await load_posts(PENDING_POSTS_FILE)
    index_str = query.data.split("_")[-1]
    index = int(index_str)
    data = await state.get_data()
    message_id = data.get("message_id")

    if len(pending_posts) > index:
      post = pending_posts[index]
    else:
        await query.answer(NOT_FOUND)
        return

    if post:
        post["admin_id"] = query.from_user.id
        post["status"] = "approved"
        
        if post.get("image") and post.get("text"):
            await bot.send_photo(CHANNEL_ID, photo=FSInputFile(post["image"]), caption=post["text"])
        elif post.get("image"):
            await bot.send_photo(CHANNEL_ID, photo=FSInputFile(post["image"]))
        elif post.get("text"):
            await bot.send_message(CHANNEL_ID, post["text"])
        
        await bot.send_message(post["user_id"], APPROVE)
        await query.answer(DONE)
    
        posts.append(post)
        await save_posts(posts, POSTS_FILE)
        pending_posts.pop(index)
        await save_posts(pending_posts, PENDING_POSTS_FILE)

    await show_posts(query.message, state, 0, message_id)
    await query.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith("reject_"))
async def admin_reject_handler(query: CallbackQuery, state: FSMContext):
    pending_posts = await load_posts(PENDING_POSTS_FILE)
    index_str = query.data.split("_")[-1]
    index = int(index_str)
    data = await state.get_data()
    message_id = data.get("message_id")
    
    if len(pending_posts) > index:
      post = pending_posts[index]
    else:
        await query.answer(NOT_FOUND)
        return
    
    if post is not None:
        post["admin_id"] = query.from_user.id
        post["status"] = "rejected"
        await bot.send_message(post["user_id"], REJECTED)
        await query.answer(UNDONE)
    
        pending_posts.pop(index)
        await save_posts(pending_posts, PENDING_POSTS_FILE)
    await show_posts(query.message, state, 0, message_id)
    await query.message.edit_reply_markup(reply_markup=None)
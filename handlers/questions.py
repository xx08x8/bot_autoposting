from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from func.states import PostState
from func.all_func import *
import os
from config.config import PENDING_POSTS_FILE, IMAGE_FOLDER
from aiogram import Bot
from aiogram.types import Message
from config.messages_list import BLACKLIST
from keyboards.keyboard import *

router = Router()

bot: Bot

def set_bot(bot_instance):
    global bot
    bot = bot_instance

@router.message(CommandStart())
async def start_handler(message: Message):
    if await is_user_blocked(message.from_user.id):
        await message.answer(BLACKLIST)
        return
    
    await message.answer(
        "⭐ Привет! Это бот для предложений постов в канал.\n\n"
        "<b>Правила форматирования:</b>\n"
        "Бот поддерживает форматирование текста с использованием HTML:\n"
        "📝 <b>Жирный текст</b>: <code>&lt;b&gt;текст&lt;/b&gt;</code>\n"
        "📝 <i>Курсив</i>: <code>&lt;i&gt;текст&lt;/i&gt;</code>\n"
        "📝 <u>Подчеркнутый</u>: <code>&lt;u&gt;текст&lt;/u&gt;</code>\n"
        "📝 <s>Зачеркнутый</s>: <code>&lt;s&gt;текст&lt;/s&gt;</code>\n"
        "📝 <tg-spoiler>Спойлер</tg-spoiler>: <code>&lt;tg-spoiler&gt;текст&lt;/tg-spoiler&gt;</code>\n"
        "📝 <u><b>Комбинации форматов</b></u>:  можно комбинировать все форматы, для примера <code>&lt;b&gt;&lt;u&gt;жирный подчеркнутый&lt;/u&gt;&lt;/b&gt;</code>\n\n"
        "\n✅ Предложить пост можно не чаще 1 раза в час, для этого нажмите кнопку ниже 👇", reply_markup=kb_offer_post()
    )

@router.message(F.text == "📨 Предложить пост")
async def suggest_post_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    logging.info(f"User {user_id} clicked 'suggest_post' button.")

    if await is_user_blocked(user_id):
        await message.answer(BLACKLIST)
        return

    can_post_bool, minutes, seconds = await can_post(user_id)
    if not can_post_bool:
        await message.answer(
            f"Вы сможете предложить пост через {minutes} мин. {seconds} сек.", 
            reply_markup=kb_offer_post()
        )
        return

    # Очистка state
    await state.clear()
    logging.info(f"Состояние создано для пользователя {user_id}.")

    await message.answer(
        "Отправьте текст и/или изображение для поста.",
        reply_markup=kb_offer_post()
    )
    await state.set_state(PostState.waiting_for_post)


@router.message(PostState.waiting_for_post)
async def get_post_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text or ""
    photo = message.photo
    file_path = None

    if photo:
        file_id = photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = os.path.join(IMAGE_FOLDER, f"{file_id}.jpg")
        await bot.download_file(file.file_path, file_path)

    if user_id != ADMIN_ID:
        user_last_post_time[user_id] = datetime.now()

    pending_posts = await load_posts(PENDING_POSTS_FILE)
    new_post = {
        "user_id": user_id,
        "image": file_path,
        "text": text,
        "status": "pending",
        "admin_id": None,
    }

    pending_posts.append(new_post)
    await save_posts(pending_posts, PENDING_POSTS_FILE)


    if user_id == ADMIN_ID:
       await bot.send_message(ADMIN_ID, "Пост от админа отправлен на проверку")
    else:
       await bot.send_message(ADMIN_ID, f"Поступило новое предложение публикации от пользователя <code>{user_id}</code>")
       await message.answer("Ваш пост отправлен на модерацию.", reply_markup=kb_offer_post())
    await state.clear()
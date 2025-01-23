import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import questions, callbacks, commands, admin
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    
    callbacks.set_bot(bot)
    questions.set_bot(bot)
    admin.set_bot(bot)
    dp.include_router(questions.router)
    dp.include_router(callbacks.router)
    dp.include_router(commands.router)
    dp.include_router(admin.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




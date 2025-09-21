import asyncio

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from database.base import create_tables
from handlers import filling_data, start_router, edit_data
from bot import bot, BASE_URL, WEBHOOK_PATH, HOST, PORT

async def set_commands():
    commands = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()
    await create_tables()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    try:
        await bot.send_message(f'Я запущен')
    except:
        pass

async def stop_bot():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.session.close()
        await bot.send_message(f'Бот остановлен')
    except:
        pass

async def main():
    dp = Dispatcher()
    dp.include_routers(start_router.router, filling_data.router, edit_data.router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot 
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=HOST, port=PORT)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
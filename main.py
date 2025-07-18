import asyncio
from aiogram import  Dispatcher
from config_reader import config
from handlers import commands, questions
from bot import bot

async def main():
    dp = Dispatcher()
    dp.include_routers(questions.router, commands.router)
        
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 
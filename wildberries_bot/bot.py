import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config import COMMANDS
from db.db import create_tables
from handlers.fsm import router_fsm
from handlers.handlers import router
from redis import asyncio as aioredis


async def main():
    await create_tables()
    bot = Bot(token=os.getenv('TOKEN'))
    redis = aioredis.Redis(host='redis')
    memory = RedisStorage(redis=redis)
    dp = Dispatcher(memory=memory)
    dp.include_routers(router, router_fsm)
    await bot.set_my_commands(commands=COMMANDS)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

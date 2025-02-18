import asyncio

from aiogram import Bot, Dispatcher
from db import init_db
from handlers import router


async def main():
    await init_db()
    bot = Bot(token="7820575438:AAFTZ2ebT2k8hMPYvjtPD3v4r5H8GWD1Jvo")
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import (
    start, calculation, subscription,
    car_selection, import_advisor, lead, profile
)
from services.storage import init_db


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # ⚠️ ВАЖЕН ПОРЯДОК:
    # 1. start       — команды /start, /contact, /cancel + главное меню
    # 2. calculation — кнопка «🚗 Рассчитать утильсбор» и вся логика
    # 3. subscription — проверка подписки на канал
    # 4. car_selection — подбор авто
    # 5. import_advisor — «Стоит ли везти?»
    # 6. lead — заявки
    # 7. profile — история расчётов
    dp.include_router(start.router)
    dp.include_router(calculation.router)
    dp.include_router(subscription.router)
    dp.include_router(car_selection.router)
    dp.include_router(import_advisor.router)
    dp.include_router(lead.router)
    dp.include_router(profile.router)

    logging.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")

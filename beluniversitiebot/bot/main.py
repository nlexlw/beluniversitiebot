"""
Главный файл запуска бота.
Регистрация роутеров и запуск polling.
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.handlers import start, calculator, universities, ai_consultant, consultation, top_specialties

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    """Основная функция запуска бота."""
    # Создаем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрируем роутеры
    dp.include_router(start.router)
    dp.include_router(calculator.router)
    dp.include_router(universities.router)
    dp.include_router(ai_consultant.router)
    dp.include_router(consultation.router)
    dp.include_router(top_specialties.router)
    
    # Запускаем polling
    logging.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен пользователем")

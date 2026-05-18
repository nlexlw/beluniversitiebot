"""
Конфигурация бота и загрузка переменных окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Токен бота (обязательно)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID администратора для получения заявок (необязательно)
ADMIN_ID = os.getenv("ADMIN_ID")
if ADMIN_ID:
    try:
        ADMIN_ID = int(ADMIN_ID)
    except ValueError:
        ADMIN_ID = None

# Username администратора для показа пользователю (необязательно)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

# Проверка наличия токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения! Создайте файл .env по примеру .env.example")

"""
Обработчик команды /start и главного меню.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.keyboards import get_main_keyboard
from bot.services.data_loader import load_universities

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработка команды /start."""
    await message.answer(
        "👋 <b>Добро пожаловать в Belarus University Guide Bot!</b>\n\n"
        "Я помогу вам:\n"
        "• Рассчитать проходной балл по ЦТ/ЦЭ\n"
        "• Подобрать ВУЗы и специальности\n"
        "• Узнать о самых востребованных направлениях\n"
        "• Получить консультацию от ИИ\n"
        "• Записаться на персональную консультацию\n\n"
        "Выберите нужный пункт в меню ниже 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "❓ Помощь")
async def help_command(message: Message):
    """Справка по боту."""
    await message.answer(
        "ℹ️ <b>Помощь по боту</b>\n\n"
        "<b>🧮 Рассчитать баллы</b>\n"
        "Пошаговый калькулятор вашего проходного балла.\n"
        "Нужны результаты 3 экзаменов и средний балл аттестата.\n\n"
        "<b>🎓 Подобрать ВУЗ</b>\n"
        "Введите ваш балл — бот покажет подходящие специальности\n"
        "на бюджет и платное, а также варианты 'почти поступил'.\n\n"
        "<b>⭐ ТОП специальностей</b>\n"
        "Самые востребованные направления по категориям.\n\n"
        "<b>🤖 ИИ-консультант</b>\n"
        "Задайте любой вопрос о поступлении — ИИ ответит.\n\n"
        "<b>📝 Записаться на консультацию</b>\n"
        "Оставьте заявку на персональную консультацию с куратором.\n\n"
        "<b>⬅️ Назад в меню</b>\n"
        "Вернуться к главному меню из любого режима.\n\n"
        "💡 <i>Данные о проходных баллах примерные.\n"
        "Всегда проверяйте информацию на официальных сайтах ВУЗов!</i>",
        parse_mode="HTML"
    )


@router.callback_query(F.data == "main_menu")
async def back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню из inline-кнопок."""
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\nВыберите нужный пункт:",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

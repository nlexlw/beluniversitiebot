"""
Обработчик ИИ-консультанта.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter

from bot.keyboards import get_ai_help_keyboard, get_main_keyboard
from bot.services.ai_service import get_ai_answer

router = Router()


@router.message(F.text == "🤖 ИИ-консультант")
async def start_ai_consultant(message: Message):
    """Запуск ИИ-консультанта."""
    await message.answer(
        "🤖 <b>ИИ-консультант по поступлению</b>\n\n"
        "Задайте ваш вопрос о поступлении в белорусские ВУЗы.\n"
        "Я постараюсь помочь!\n\n"
        "<i>⚠️ Важно: Я не являюсь официальной приёмной комиссией.\n"
        "Всегда проверяйте информацию на официальных сайтах ВУЗов.</i>\n\n"
        "⬅️ Нажмите 'Назад в меню' для выхода.",
        reply_markup=get_ai_help_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "⬅️ Назад в меню")
async def back_from_ai(message: Message):
    """Выход из режима ИИ-консультанта."""
    # Проверяем, что пользователь действительно в режиме ИИ
    # (это упрощённая проверка, в production лучше использовать FSM)
    await message.answer(
        "🏠 <b>Главное меню</b>",
        reply_markup=get_main_keyboard()
    )


@router.message(~F.text.startswith("⬅️"))
async def handle_ai_question(message: Message):
    """Обработка вопроса к ИИ."""
    # Пропускаем системные команды и кнопки
    if message.text in ["🧮 Рассчитать баллы", "🎓 Подобрать ВУЗ", 
                        "⭐ ТОП специальностей", "📝 Записаться на консультацию",
                        "❓ Помощь", "🤖 ИИ-консультант"]:
        return
    
    question = message.text.strip()
    
    # Отправляем сообщение "печатает..."
    await message.answer_chat_action("typing")
    
    # Получаем ответ от ИИ
    answer = await get_ai_answer(question)
    
    await message.answer(
        answer,
        reply_markup=get_ai_help_keyboard(),
        parse_mode="HTML"
    )

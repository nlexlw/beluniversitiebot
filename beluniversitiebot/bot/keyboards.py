"""
Клавиатуры для бота (inline и reply).
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню бота."""
    keyboard = [
        [KeyboardButton(text="🧮 Рассчитать баллы")],
        [KeyboardButton(text="🎓 Подобрать ВУЗ")],
        [KeyboardButton(text="⭐ ТОП специальностей")],
        [KeyboardButton(text="🤖 ИИ-консультант")],
        [KeyboardButton(text="📝 Записаться на консультацию")],
        [KeyboardButton(text="❓ Помощь")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_back_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой 'Назад'."""
    keyboard = [
        [KeyboardButton(text="⬅️ Назад в меню")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_university_result_keyboard(user_score: int) -> InlineKeyboardMarkup:
    """Клавиатура для результатов подбора ВУЗа."""
    keyboard = [
        [InlineKeyboardButton(text="🔄 Подобрать ещё раз", callback_data="match_universities")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_calculator_result_keyboard(score: int) -> InlineKeyboardMarkup:
    """Клавиатура после расчёта баллов."""
    keyboard = [
        [InlineKeyboardButton(text="🎓 Подобрать ВУЗ по этим баллам", callback_data=f"match_with_score:{score}")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_top_specialties_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для ТОП специальностей."""
    keyboard = [
        [InlineKeyboardButton(text="💻 IT / Программирование", callback_data="top_category:IT")],
        [InlineKeyboardButton(text="⚙️ Инженерия", callback_data="top_category:Engineering")],
        [InlineKeyboardButton(text="📊 Экономика / Менеджмент", callback_data="top_category:Economics")],
        [InlineKeyboardButton(text="🏥 Медицина / Биология", callback_data="top_category:Medicine")],
        [InlineKeyboardButton(text="📚 Педагогика", callback_data="top_category:Pedagogy")],
        [InlineKeyboardButton(text="📖 Гуманитарные науки", callback_data="top_category:Humanities")],
        [InlineKeyboardButton(text="🏆 Все специальности", callback_data="top_all")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_consultation_confirm_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения записи на консультацию."""
    keyboard = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="consultation_confirm")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="consultation_cancel")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_ai_help_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для ИИ-консультанта."""
    keyboard = [
        [KeyboardButton(text="⬅️ Назад в меню")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

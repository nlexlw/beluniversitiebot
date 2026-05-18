"""
Обработчик ТОП специальностей.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards import get_top_specialties_keyboard, get_main_keyboard
from bot.services.university_matcher import get_top_specialties_by_category, get_specialties_grouped_by_category

router = Router()


@router.message(F.text == "⭐ ТОП специальностей")
async def show_top_categories(message: Message):
    """Показ категорий ТОП специальностей."""
    await message.answer(
        "🏆 <b>ТОП востребованных специальностей</b>\n\n"
        "Выберите категорию для просмотра:\n\n"
        "<i>Специальности отсортированы по уровню спроса и проходным баллам.</i>",
        reply_markup=get_top_specialties_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("top_category:"))
async def show_category_specialties(callback: CallbackQuery):
    """Показ специальностей выбранной категории."""
    category = callback.data.split(":")[1]
    
    category_names = {
        "IT": "💻 IT / Программирование",
        "Engineering": "⚙️ Инженерия",
        "Economics": "📊 Экономика / Менеджмент",
        "Medicine": "🏥 Медицина / Биология",
        "Pedagogy": "📚 Педагогика",
        "Humanities": "📖 Гуманитарные науки"
    }
    
    specialties = get_top_specialties_by_category(category, limit=10)
    
    if not specialties:
        await callback.answer("В этой категории пока нет данных", show_alert=True)
        return
    
    result_text = f"<b>{category_names.get(category, category)}</b>\n\n"
    
    for i, spec in enumerate(specialties, 1):
        demand_emoji = {"high": "🔥", "medium": "⚡", "low": "💡"}.get(
            spec.get("demand_level", "low"), "•"
        )
        
        result_text += f"{i}. {demand_emoji} <b>{spec['specialty']}</b>\n"
        result_text += f"   🏫 {spec['university']}\n"
        result_text += f"   📊 Бюджет: {spec.get('budget_passing_score_2024', 'н/д')}\n"
        result_text += f"   💰 Платное: {spec.get('paid_passing_score_2024', 'н/д')}\n"
        
        if spec.get("description"):
            desc = spec["description"][:80] + "..." if len(spec["description"]) > 80 else spec["description"]
            result_text += f"   💡 {desc}\n"
        
        result_text += "\n"
    
    # Добавляем кнопку назад
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад к категориям", callback_data="top_back")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ])
    
    await callback.message.edit_text(result_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "top_all")
async def show_all_top_specialties(callback: CallbackQuery):
    """Показ всех ТОП специальностей."""
    grouped = get_specialties_grouped_by_category()
    
    category_names = {
        "IT": "💻 IT / Программирование",
        "Engineering": "⚙️ Инженерия",
        "Economics": "📊 Экономика / Менеджмент",
        "Medicine": "🏥 Медицина / Биология",
        "Pedagogy": "📚 Педагогика",
        "Humanities": "📖 Гуманитарные науки"
    }
    
    result_text = "🏆 <b>Все специальности по категориям</b>\n\n"
    
    for category, specs in grouped.items():
        cat_name = category_names.get(category, category)
        result_text += f"\n<b>{cat_name}</b>\n"
        
        # Показываем топ-3 из каждой категории
        for spec in specs[:3]:
            demand_emoji = {"high": "🔥", "medium": "⚡", "low": "💡"}.get(
                spec.get("demand_level", "low"), "•"
            )
            result_text += f"  {demand_emoji} {spec['specialty']} ({spec.get('budget_passing_score_2024', 'н/д')})\n"
    
    result_text += "\n<i>Выберите конкретную категорию для подробного просмотра.</i>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Категории", callback_data="top_back")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ])
    
    await callback.message.edit_text(result_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "top_back")
async def back_to_categories(callback: CallbackQuery):
    """Возврат к списку категорий."""
    await callback.message.edit_text(
        "🏆 <b>ТОП востребованных специальностей</b>\n\n"
        "Выберите категорию для просмотра:",
        reply_markup=get_top_specialties_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

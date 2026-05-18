"""
Обработчик подбора ВУЗов.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_back_keyboard, get_university_result_keyboard
from bot.services.university_matcher import find_matching_specialties, format_specialty_list

router = Router()


@router.message(F.text == "🎓 Подобрать ВУЗ")
async def start_university_search(message: Message, state: FSMContext):
    """Начало поиска ВУЗа."""
    await state.set_state("waiting_for_score_input")
    await message.answer(
        "🔍 <b>Подбор ВУЗа по баллам</b>\n\n"
        "Введите ваш <b>итоговый проходной балл</b>:\n"
        "(например, 320)\n\n"
        "⬅️ Нажмите 'Назад в меню' для отмены.",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text == "⬅️ Назад в меню")
async def back_to_menu_from_anywhere(message: Message, state: FSMContext):
    """Возврат в главное меню из любого состояния."""
    await state.clear()
    from bot.keyboards import get_main_keyboard
    await message.answer(
        "🏠 <b>Главное меню</b>",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text.isdigit())
async def process_score_input(message: Message, state: FSMContext):
    """Обработка введённого балла для подбора ВУЗа."""
    current_state = await state.get_state()
    
    # Проверяем, что мы в состоянии ожидания балла
    if current_state != "waiting_for_score_input":
        return
    
    try:
        score = int(message.text.strip())
        if score < 0 or score > 400:
            raise ValueError()
    except (ValueError, TypeError):
        await message.answer(
            "❌ Некорректное значение. Введите число от 0 до 400."
        )
        return

    await show_university_results(message, score, state)


async def show_university_results(message: Message, score: int, state: FSMContext):
    """Показ результатов подбора ВУЗов."""
    await state.clear()
    
    # Находим подходящие специальности
    budget_matches, paid_matches, near_misses = find_matching_specialties(score)
    
    if not budget_matches and not paid_matches and not near_misses:
        await message.answer(
            f"😔 К сожалению, с баллом <b>{score}</b> не найдено подходящих специальностей.\n\n"
            "Попробуйте:\n"
            "• Пересдать экзамены\n"
            "• Рассмотреть платные отделения других ВУЗов\n"
            "• Обратиться за консультацией к куратору",
            reply_markup=get_university_result_keyboard(score),
            parse_mode="HTML"
        )
        return
    
    result_text = f"🎓 <b>Результаты подбора для {score} баллов</b>\n\n"
    
    # Бюджетные места
    if budget_matches:
        result_text += "✅ <b>Бюджет (проходите):</b>\n"
        result_text += format_specialty_list(budget_matches[:5], "budget")
        if len(budget_matches) > 5:
            result_text += f"... и ещё {len(budget_matches) - 5} специальностей\n\n"
        else:
            result_text += "\n"
    else:
        result_text += "❌ <b>Бюджет:</b> нет подходящих специальностей\n\n"
    
    # Платные места
    if paid_matches:
        result_text += "💰 <b>Платное (проходите):</b>\n"
        result_text += format_specialty_list(paid_matches[:5], "paid")
        if len(paid_matches) > 5:
            result_text += f"... и ещё {len(paid_matches) - 5} специальностей\n\n"
        else:
            result_text += "\n"
    else:
        result_text += "❌ <b>Платное:</b> нет подходящих специальностей\n\n"
    
    # Почти поступил
    if near_misses:
        result_text += "⚠️ <b>Почти поступил (не хватает до 20 баллов):</b>\n"
        result_text += format_specialty_list(near_misses[:5], "near")
        if len(near_misses) > 5:
            result_text += f"... и ещё {len(near_misses) - 5} специальностей\n\n"
        else:
            result_text += "\n"
    
    result_text += (
        "<i>💡 Проходные баллы могут меняться каждый год.\n"
        "Уточняйте актуальную информацию на сайтах ВУЗов.</i>"
    )
    
    await message.answer(
        result_text,
        reply_markup=get_university_result_keyboard(score),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "match_universities")
async def retry_match(callback: CallbackQuery, state: FSMContext):
    """Повторный подбор ВУЗа."""
    await state.set_state("waiting_for_score_input")
    await callback.message.edit_text(
        "🔍 <b>Подбор ВУЗа по баллам</b>\n\n"
        "Введите ваш <b>итоговый проходной балл</b>:\n"
        "(например, 320)",
        parse_mode="HTML"
    )
    await callback.answer()

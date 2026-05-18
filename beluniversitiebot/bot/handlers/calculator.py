"""
Обработчик калькулятора баллов (FSM).
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import ScoreCalculator
from bot.keyboards import get_back_keyboard, get_calculator_result_keyboard
from bot.services.score_calculator import validate_score, calculate_total_score

router = Router()


@router.message(F.text == "🧮 Рассчитать баллы")
async def start_calculator(message: Message, state: FSMContext):
    """Начало расчёта баллов."""
    await state.set_state(ScoreCalculator.waiting_for_exam1)
    await message.answer(
        "📝 <b>Калькулятор проходного балла</b>\n\n"
        "Введите результат <b>первого экзамена</b> (ЦТ/ЦЭ):\n"
        "Значение от 0 до 100.\n\n"
        "⬅️ Нажмите 'Назад в меню' для отмены.",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )


@router.message(ScoreCalculator.waiting_for_exam1, F.text != "⬅️ Назад в меню")
async def process_exam1(message: Message, state: FSMContext):
    """Обработка первого экзамена."""
    try:
        score = int(message.text.strip())
        if not validate_score(score, 0, 100):
            raise ValueError()
    except (ValueError, TypeError):
        await message.answer(
            "❌ Некорректное значение. Введите число от 0 до 100."
        )
        return

    await state.update_data(exam1=score)
    await state.set_state(ScoreCalculator.waiting_for_exam2)
    await message.answer(
        f"✅ Первый экзамен: {score} баллов\n\n"
        "Введите результат <b>второго экзамена</b> (ЦТ/ЦЭ):\n"
        "Значение от 0 до 100.",
        parse_mode="HTML"
    )


@router.message(ScoreCalculator.waiting_for_exam2, F.text != "⬅️ Назад в меню")
async def process_exam2(message: Message, state: FSMContext):
    """Обработка второго экзамена."""
    try:
        score = int(message.text.strip())
        if not validate_score(score, 0, 100):
            raise ValueError()
    except (ValueError, TypeError):
        await message.answer(
            "❌ Некорректное значение. Введите число от 0 до 100."
        )
        return

    await state.update_data(exam2=score)
    await state.set_state(ScoreCalculator.waiting_for_exam3)
    await message.answer(
        f"✅ Второй экзамен: {score} баллов\n\n"
        "Введите результат <b>третьего экзамена</b> (ЦТ/ЦЭ):\n"
        "Значение от 0 до 100.\n"
        "<i>Если экзаменов только 2, введите 0.</i>",
        parse_mode="HTML"
    )


@router.message(ScoreCalculator.waiting_for_exam3, F.text != "⬅️ Назад в меню")
async def process_exam3(message: Message, state: FSMContext):
    """Обработка третьего экзамена."""
    try:
        score = int(message.text.strip())
        if not validate_score(score, 0, 100):
            raise ValueError()
    except (ValueError, TypeError):
        await message.answer(
            "❌ Некорректное значение. Введите число от 0 до 100."
        )
        return

    await state.update_data(exam3=score)
    await state.set_state(ScoreCalculator.waiting_for_certificate)
    await message.answer(
        f"✅ Третий экзамен: {score} баллов\n\n"
        "Введите <b>средний балл аттестата</b>:\n"
        "Значение от 1.0 до 10.0\n"
        "Можно с десятичной дробью (например, 7.5)",
        parse_mode="HTML"
    )


@router.message(ScoreCalculator.waiting_for_certificate, F.text != "⬅️ Назад в меню")
async def process_certificate(message: Message, state: FSMContext):
    """Обработка среднего балла аттестата и расчёт итогового балла."""
    try:
        # Заменяем запятую на точку для поддержки русского формата
        cert_text = message.text.strip().replace(",", ".")
        cert_score = float(cert_text)
        if not validate_score(cert_score, 1.0, 10.0):
            raise ValueError()
    except (ValueError, TypeError):
        await message.answer(
            "❌ Некорректное значение. Введите число от 1.0 до 10.0"
        )
        return

    # Получаем все данные
    data = await state.get_data()
    exam1 = data["exam1"]
    exam2 = data["exam2"]
    exam3 = data["exam3"]

    # Рассчитываем итоговый балл
    total_score = calculate_total_score(exam1, exam2, exam3, cert_score)

    # Очищаем состояние
    await state.clear()

    # Формируем сообщение с результатом
    result_text = (
        "🎉 <b>Расчёт завершён!</b>\n\n"
        f"📊 Ваши результаты:\n"
        f"• Первый экзамен: {exam1}\n"
        f"• Второй экзамен: {exam2}\n"
        f"• Третий экзамен: {exam3}\n"
        f"• Средний балл аттестата: {cert_score:.1f}\n\n"
        f"🏆 <b>Итоговый проходной балл: {total_score}</b>\n\n"
        f"<i>Формула: ЦТ1 + ЦТ2 + ЦТ3 + (средний балл × 10)</i>\n\n"
        "Теперь вы можете подобрать ВУЗы по этому баллу!"
    )

    await message.answer(
        result_text,
        reply_markup=get_calculator_result_keyboard(total_score),
        parse_mode="HTML"
    )


@router.message(ScoreCalculator.waiting_for_exam1, F.text == "⬅️ Назад в меню")
@router.message(ScoreCalculator.waiting_for_exam2, F.text == "⬅️ Назад в меню")
@router.message(ScoreCalculator.waiting_for_exam3, F.text == "⬅️ Назад в меню")
@router.message(ScoreCalculator.waiting_for_certificate, F.text == "⬅️ Назад в меню")
async def cancel_calculator(message: Message, state: FSMContext):
    """Отмена расчёта и возврат в меню."""
    await state.clear()
    from bot.keyboards import get_main_keyboard
    await message.answer(
        "❌ Расчёт отменён.\n\nВыберите пункт меню:",
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data.startswith("match_with_score:"))
async def match_with_score_callback(callback: CallbackQuery, state: FSMContext):
    """Переход к подбору ВУЗа с указанным баллом."""
    score = int(callback.data.split(":")[1])
    await state.update_data(user_score=score)
    
    # Импортируем здесь, чтобы избежать циклического импорта
    from bot.handlers.universities import show_university_results
    
    await show_university_results(callback.message, score, state)
    await callback.answer()

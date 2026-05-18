"""
Обработчик записи на консультацию.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.states import ConsultationRequest
from bot.keyboards import get_back_keyboard, get_consultation_confirm_keyboard, get_main_keyboard
from bot.config import ADMIN_ID, ADMIN_USERNAME

router = Router()


@router.message(F.text == "📝 Записаться на консультацию")
async def start_consultation(message: Message, state: FSMContext):
    """Начало записи на консультацию."""
    await state.set_state(ConsultationRequest.waiting_for_name)
    await message.answer(
        "📝 <b>Запись на персональную консультацию</b>\n\n"
        "Введите ваше <b>имя</b>:\n\n"
        "⬅️ Нажмите 'Назад в меню' для отмены.",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )


@router.message(ConsultationRequest.waiting_for_name, F.text != "⬅️ Назад в меню")
async def process_name(message: Message, state: FSMContext):
    """Обработка имени."""
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("❌ Введите корректное имя (минимум 2 символа).")
        return
    
    await state.update_data(name=name)
    await state.set_state(ConsultationRequest.waiting_for_grade)
    await message.answer(
        f"✅ Имя: {name}\n\n"
        "Введите ваш <b>класс/курс</b>:\n"
        "(например, 11 класс, 9 класс, абитуриент)",
        parse_mode="HTML"
    )


@router.message(ConsultationRequest.waiting_for_grade, F.text != "⬅️ Назад в меню")
async def process_grade(message: Message, state: FSMContext):
    """Обработка класса/курса."""
    grade = message.text.strip()
    if len(grade) < 2:
        await message.answer("❌ Введите корректный класс/курс.")
        return
    
    await state.update_data(grade=grade)
    await state.set_state(ConsultationRequest.waiting_for_field)
    await message.answer(
        f"✅ Класс/курс: {grade}\n\n"
        "Какое <b>направление или ВУЗ</b> вас интересует?\n"
        "(например: IT, медицина, БГУ, не определился)",
        parse_mode="HTML"
    )


@router.message(ConsultationRequest.waiting_for_field, F.text != "⬅️ Назад в меню")
async def process_field(message: Message, state: FSMContext):
    """Обработка направления."""
    field = message.text.strip()
    if len(field) < 2:
        await message.answer("❌ Введите корректное направление.")
        return
    
    await state.update_data(field=field)
    await state.set_state(ConsultationRequest.waiting_for_contact)
    await message.answer(
        f"✅ Направление: {field}\n\n"
        "Оставьте ваш <b>вопрос или контактную информацию</b>:\n"
        "(Telegram, телефон, email, или ваш вопрос)",
        parse_mode="HTML"
    )


@router.message(ConsultationRequest.waiting_for_contact, F.text != "⬅️ Назад в меню")
async def process_contact(message: Message, state: FSMContext):
    """Обработка контакта и завершение заявки."""
    contact = message.text.strip()
    if len(contact) < 5:
        await message.answer("❌ Введите более подробную информацию.")
        return
    
    # Получаем все данные
    data = await state.get_data()
    
    # Формируем сообщение для админа
    request_text = (
        "📩 <b>Новая заявка на консультацию!</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📚 Класс/курс: {data['grade']}\n"
        f"🎯 Направление: {data['field']}\n"
        f"📞 Контакт: {contact}\n\n"
        f"ID пользователя: {message.from_user.id}\n"
        f"Username: @{message.from_user.username or 'нет'}"
    )
    
    # Сохраняем данные для подтверждения
    await state.update_data(contact=contact, request_text=request_text)
    await state.set_state("waiting_for_confirmation")
    
    await message.answer(
        "✅ <b>Данные получены!</b>\n\n"
        "Проверьте информацию:\n\n"
        f"• Имя: {data['name']}\n"
        f"• Класс/курс: {data['grade']}\n"
        f"• Направление: {data['field']}\n"
        f"• Контакт: {contact}\n\n"
        "Подтвердите отправку заявки:",
        reply_markup=get_consultation_confirm_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "consultation_confirm")
async def confirm_consultation(callback: CallbackQuery, state: FSMContext):
    """Подтверждение и отправка заявки."""
    data = await state.get_data()
    
    # Отправляем заявку админу (если ID указан)
    if ADMIN_ID:
        try:
            await callback.bot.send_message(
                chat_id=ADMIN_ID,
                text=data["request_text"],
                parse_mode="HTML"
            )
            admin_sent = True
        except Exception as e:
            admin_sent = False
    else:
        admin_sent = False
    
    # Очищаем состояние
    await state.clear()
    
    # Формируем ответ пользователю
    if admin_sent:
        response_text = (
            "✅ <b>Заявка отправлена!</b>\n\n"
            "Администратор получит вашу заявку в ближайшее время.\n"
            "Ожидайте связи!\n\n"
        )
    else:
        response_text = (
            "✅ <b>Заявка сохранена!</b>\n\n"
            "К сожалению, не удалось отправить уведомление администратору.\n"
            "Но вы можете связаться самостоятельно:\n\n"
        )
    
    if ADMIN_USERNAME:
        response_text += f"📲 Telegram: @{ADMIN_USERNAME}\n\n"
    
    response_text += "Спасибо за обращение! 🙏"
    
    await callback.message.edit_text(
        response_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "consultation_cancel")
async def cancel_consultation(callback: CallbackQuery, state: FSMContext):
    """Отмена заявки."""
    await state.clear()
    await callback.message.edit_text(
        "❌ Заявка отменена.\n\nВыберите пункт меню:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.message(ConsultationRequest.waiting_for_name, F.text == "⬅️ Назад в меню")
@router.message(ConsultationRequest.waiting_for_grade, F.text == "⬅️ Назад в меню")
@router.message(ConsultationRequest.waiting_for_field, F.text == "⬅️ Назад в меню")
@router.message(ConsultationRequest.waiting_for_contact, F.text == "⬅️ Назад в меню")
async def cancel_consultation_flow(message: Message, state: FSMContext):
    """Отмена записи на консультацию."""
    await state.clear()
    await message.answer(
        "❌ Запись отменена.\n\nВыберите пункт меню:",
        reply_markup=get_main_keyboard()
    )

"""
FSM состояния для калькулятора баллов и других пошаговых процессов.
"""

from aiogram.fsm.state import State, StatesGroup


class ScoreCalculator(StatesGroup):
    """Состояния для калькулятора баллов."""
    waiting_for_exam1 = State()  # Первый экзамен
    waiting_for_exam2 = State()  # Второй экзамен
    waiting_for_exam3 = State()  # Третий экзамен
    waiting_for_certificate = State()  # Средний балл аттестата


class ConsultationRequest(StatesGroup):
    """Состояния для записи на консультацию."""
    waiting_for_name = State()  # Имя
    waiting_for_grade = State()  # Класс/курс
    waiting_for_field = State()  # Желаемое направление
    waiting_for_contact = State()  # Контактная информация/вопрос

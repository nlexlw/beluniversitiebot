"""
Сервис расчёта проходных баллов.
"""


def validate_score(score: float, min_val: float, max_val: float) -> bool:
    """
    Проверка корректности балла.
    
    Args:
        score: Значение балла
        min_val: Минимально допустимое значение
        max_val: Максимально допустимое значение
    
    Returns:
        True если балл в допустимом диапазоне
    """
    return min_val <= score <= max_val


def calculate_total_score(exam1: int, exam2: int, exam3: int, certificate_avg: float) -> int:
    """
    Расчёт итогового проходного балла.
    
    Формула: ЦТ1 + ЦТ2 + ЦТ3 + (средний балл аттестата × 10)
    
    Args:
        exam1: Результат первого экзамена (0-100)
        exam2: Результат второго экзамена (0-100)
        exam3: Результат третьего экзамена (0-100)
        certificate_avg: Средний балл аттестата (1.0-10.0)
    
    Returns:
        Итоговый проходной балл (целое число)
    """
    total = exam1 + exam2 + exam3 + (certificate_avg * 10)
    return int(round(total))

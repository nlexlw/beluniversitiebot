"""
Сервис подбора ВУЗов и специальностей.
"""

from bot.services.data_loader import load_universities


def find_matching_specialties(user_score: int):
    """
    Поиск подходящих специальностей по баллу пользователя.
    
    Args:
        user_score: Итоговый балл пользователя
    
    Returns:
        Кортеж из трёх списков:
        - budget_matches: специальности на бюджет
        - paid_matches: специальности на платное
        - near_misses: специальности где не хватает до 20 баллов
    """
    universities = load_universities()
    
    budget_matches = []
    paid_matches = []
    near_misses = []
    
    for uni in universities:
        budget_score = uni.get("budget_passing_score_2024", 999)
        paid_score = uni.get("paid_passing_score_2024", 999)
        
        # Проверяем бюджет
        if user_score >= budget_score:
            budget_matches.append({
                **uni,
                "match_type": "budget",
                "passing_score": budget_score
            })
        # Проверяем платное
        elif user_score >= paid_score:
            paid_matches.append({
                **uni,
                "match_type": "paid",
                "passing_score": paid_score
            })
        # Проверяем "почти поступил" (не хватает до 20 баллов до бюджета)
        elif budget_score - user_score <= 20:
            near_misses.append({
                **uni,
                "match_type": "near",
                "passing_score": budget_score,
                "missing_points": budget_score - user_score
            })
    
    # Сортируем по проходному баллу (убывание)
    budget_matches.sort(key=lambda x: x["passing_score"], reverse=True)
    paid_matches.sort(key=lambda x: x["passing_score"], reverse=True)
    near_misses.sort(key=lambda x: x["passing_score"], reverse=True)
    
    return budget_matches, paid_matches, near_misses


def format_specialty_list(specialties: list, match_type: str) -> str:
    """
    Форматирование списка специальностей для вывода.
    
    Args:
        specialties: Список специальностей
        match_type: Тип соответствия (budget, paid, near)
    
    Returns:
        Отформатированная строка со списком специальностей
    """
    if not specialties:
        return ""
    
    result = ""
    emoji = {"budget": "✅", "paid": "💰", "near": "⚠️"}.get(match_type, "•")
    
    for spec in specialties:
        result += f"{emoji} <b>{spec['specialty']}</b>\n"
        result += f"   🏫 {spec['university']}\n"
        result += f"   📍 {spec['faculty']}\n"
        result += f"   🌆 {spec['city']}\n"
        
        if match_type == "near":
            result += f"   ❗ Не хватает {spec['missing_points']} баллов до бюджета\n"
        else:
            score_type = "бюджет" if match_type == "budget" else "платное"
            result += f"   📊 Проходной ({score_type}): {spec['passing_score']}\n"
        
        if spec.get("description"):
            result += f"   💡 {spec['description'][:100]}{'...' if len(spec['description']) > 100 else ''}\n"
        
        result += "\n"
    
    return result


def get_top_specialties_by_category(category: str = None, limit: int = 10):
    """
    Получение ТОП специальностей по категории или всех подряд.
    
    Args:
        category: Категория (IT, Engineering, Economics, Medicine, Pedagogy, Humanities)
        limit: Максимальное количество результатов
    
    Returns:
        Список специальностей, отсортированный по уровню востребованности
    """
    universities = load_universities()
    
    # Фильтруем по категории если указана
    if category:
        filtered = [u for u in universities if u.get("category") == category]
    else:
        filtered = universities
    
    # Сортируем по demand_level (high > medium > low)
    demand_order = {"high": 0, "medium": 1, "low": 2}
    filtered.sort(key=lambda x: (demand_order.get(x.get("demand_level", "low"), 3), 
                                  -x.get("budget_passing_score_2024", 0)))
    
    return filtered[:limit]


def get_specialties_grouped_by_category():
    """
    Группировка специальностей по категориям.
    
    Returns:
        dict: {category: [список специальностей]}
    """
    universities = load_universities()
    
    grouped = {}
    for uni in universities:
        category = uni.get("category", "Other")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(uni)
    
    # Сортируем внутри каждой категории по востребованности
    demand_order = {"high": 0, "medium": 1, "low": 2}
    for category in grouped:
        grouped[category].sort(
            key=lambda x: (demand_order.get(x.get("demand_level", "low"), 3),
                          -x.get("budget_passing_score_2024", 0))
        )
    
    return grouped

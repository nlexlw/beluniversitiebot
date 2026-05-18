"""
Сервис загрузки данных из JSON файлов.
"""

import json
import os
from typing import List, Dict


def get_data_path() -> str:
    """
    Получение пути к директории data.
    
    Returns:
        Абсолютный путь к директории data
    """
    # Путь от корня проекта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(project_root, "data")
    return data_path


def load_universities() -> List[Dict]:
    """
    Загрузка данных о ВУЗах из JSON файла.
    
    Returns:
        Список словарей с данными о ВУЗах и специальностях
    """
    data_path = get_data_path()
    json_file = os.path.join(data_path, "universities_2024.json")
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"Warning: Expected list in {json_file}, got {type(data)}")
            return []
        
        return data
    
    except FileNotFoundError:
        print(f"Error: File {json_file} not found!")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file {json_file}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error loading {json_file}: {e}")
        return []


def save_universities(data: List[Dict]) -> bool:
    """
    Сохранение данных о ВУЗах в JSON файл.
    
    Args:
        data: Список словарей с данными
    
    Returns:
        True если сохранение успешно
    """
    data_path = get_data_path()
    json_file = os.path.join(data_path, "universities_2024.json")
    
    try:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {json_file}: {e}")
        return False


def get_unique_cities() -> List[str]:
    """
    Получение списка уникальных городов из данных.
    
    Returns:
        Список названий городов
    """
    universities = load_universities()
    cities = set()
    
    for uni in universities:
        city = uni.get("city")
        if city:
            cities.add(city)
    
    return sorted(list(cities))


def get_unique_universities() -> List[str]:
    """
    Получение списка уникальных ВУЗов.
    
    Returns:
        Список названий ВУЗов
    """
    universities = load_universities()
    unis = set()
    
    for uni in universities:
        name = uni.get("university")
        if name:
            unis.add(name)
    
    return sorted(list(unis))


def get_categories() -> List[str]:
    """
    Получение списка категорий специальностей.
    
    Returns:
        Список категорий
    """
    universities = load_universities()
    categories = set()
    
    for uni in universities:
        category = uni.get("category")
        if category:
            categories.add(category)
    
    # Возвращаем в определённом порядке
    order = ["IT", "Engineering", "Economics", "Medicine", "Pedagogy", "Humanities"]
    result = []
    
    for cat in order:
        if cat in categories:
            result.append(cat)
    
    # Добавляем остальные категории если есть
    for cat in sorted(categories):
        if cat not in result:
            result.append(cat)
    
    return result

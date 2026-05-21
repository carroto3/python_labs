"""
Модуль сохранения и загрузки данных.
Предметная область: Недвижимость.

Обеспечивает сохранение коллекции объектов недвижимости в JSON-файл
и последующую загрузку с восстановлением правильных типов объектов
(полиморфная десериализация через фабрику apartment_from_dict).
"""

import json
import os
from typing import Any

from models import Apartment, apartment_from_dict
from exceptions import StorageError


def save(collection: list[Apartment], filepath: str) -> None:
    """
    Сохраняет коллекцию объектов недвижимости в JSON-файл.

    Каждый объект сериализуется через метод to_dict(),
    который сохраняет тип объекта в поле 'type' для последующего
    восстановления полиморфной иерархии.

    Args:
        collection: список объектов Apartment (включая производные классы)
                    для сохранения.
        filepath: путь к файлу для сохранения данных.

    Raises:
        StorageError: если не удалось записать файл (оборачивает IOError).
    """
    data: list[dict[str, Any]] = [item.to_dict() for item in collection]
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except IOError as exc:
        raise StorageError(
            f"Не удалось сохранить данные в файл '{filepath}': {exc}"
        ) from exc


def load(filepath: str) -> list[Apartment]:
    """
    Загружает объекты недвижимости из JSON-файла.

    Автоматически восстанавливает правильные типы объектов
    (Apartment, ResidentialApartment, CommercialApartment)
    через фабричную функцию apartment_from_dict.

    Args:
        filepath: путь к JSON-файлу с данными.

    Returns:
        list[Apartment]: список восстановленных объектов недвижимости.

    Raises:
        FileNotFoundError: если файл не существует.
        StorageError: если не удалось прочитать файл.
        ValueError: если данные в файле повреждены или имеют неверный формат.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Файл данных не найден: '{filepath}'"
        )

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            raw_data: Any = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Ошибка чтения JSON из файла '{filepath}': {exc}"
        ) from exc
    except IOError as exc:
        raise StorageError(
            f"Не удалось прочитать файл '{filepath}': {exc}"
        ) from exc

    if not isinstance(raw_data, list):
        raise ValueError(
            f"Ожидался список объектов в файле '{filepath}', "
            f"получен {type(raw_data).__name__}"
        )

    collection: list[Apartment] = []
    for index, item_data in enumerate(raw_data):
        if not isinstance(item_data, dict):
            raise ValueError(
                f"Элемент {index} в файле '{filepath}' "
                f"не является словарём (получен {type(item_data).__name__})"
            )
        apartment: Apartment = apartment_from_dict(item_data)
        collection.append(apartment)

    return collection

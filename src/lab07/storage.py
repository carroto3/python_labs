"""
Модуль сохранения и загрузки данных.
Обеспечивает персистентность коллекции объектов недвижимости через JSON.
Поддерживает полиморфную десериализацию.
"""

import json
import os
from typing import List

from models import Apartment, create_apartment_from_dict
from exceptions import StorageError


class Storage:
    """Класс для работы с файловым хранилищем (JSON).

    Attributes:
        filepath (str): путь к JSON-файлу данных.
    """

    def __init__(self, filepath: str) -> None:
        """Инициализация хранилища.

        Args:
            filepath (str): путь к JSON-файлу.
        """
        self.filepath = filepath

    def save(self, items: List[Apartment]) -> None:
        """Сохраняет коллекцию объектов в JSON-файл.

        Args:
            items (List[Apartment]): коллекция для сохранения.

        Raises:
            StorageError: если запись не удалась.
        """
        try:
            data = [item.to_dict() for item in items]
            directory = os.path.dirname(self.filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except (IOError, OSError, PermissionError) as e:
            raise StorageError(
                self.filepath,
                f"Не удалось сохранить данные: {e}",
            ) from e

    def load(self) -> List[Apartment]:
        """Загружает коллекцию объектов из JSON-файла.

        Если файл не существует, возвращает пустой список.

        Returns:
            List[Apartment]: загруженная коллекция.

        Raises:
            StorageError: если чтение или разбор не удались.
        """
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except (IOError, OSError, PermissionError) as e:
            raise StorageError(
                self.filepath,
                f"Не удалось прочитать файл: {e}",
            ) from e
        except json.JSONDecodeError as e:
            raise StorageError(
                self.filepath,
                f"Файл повреждён (некорректный JSON): {e}",
            ) from e

        items: List[Apartment] = []
        for entry in raw_data:
            try:
                item = create_apartment_from_dict(entry)
                items.append(item)
            except (TypeError, ValueError) as e:
                print(f"Предупреждение: пропущена повреждённая запись: {e}")

        return items

    def delete_file(self) -> None:
        """Удаляет файл данных."""
        if os.path.exists(self.filepath):
            try:
                os.remove(self.filepath)
            except OSError as e:
                raise StorageError(
                    self.filepath,
                    f"Не удалось удалить файл: {e}",
                ) from e

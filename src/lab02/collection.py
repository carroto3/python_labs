"""
Модуль коллекции для управления квартирами.
Предметная область: Недвижимость.
"""

from model import Apartment


class ApartmentCollection:
    """
    Класс-коллекция для управления множеством квартир.
    """

    def __init__(self):
        """
        Инициализирует пустую коллекцию квартир.
        """
        self._items = []

    def add(self, item):
        """
        Добавляет квартиру в коллекцию.

        Args:
            item: объект квартиры для добавления.

        Raises:
            TypeError: если передан объект, не являющийся экземпляром Apartment.
        """
        if not isinstance(item, Apartment):
            raise TypeError(
                f"Можно добавлять только объекты типа Apartment, "
                f"получен {type(item).__name__}"
            )
        self._items.append(item)

    def remove(self, item):
        """
        Удаляет квартиру из коллекции.

        Args:
            item: объект квартиры для удаления.

        Raises:
            TypeError : если передан объект неверного типа.
            ValueError: если объект не найден в коллекции.
        """
        if not isinstance(item, Apartment):
            raise TypeError(
                f"Можно удалять только объекты типа Apartment, "
                f"получен {type(item).__name__}"
            )
        if item not in self._items:
            raise ValueError(
                f"Квартира не найдена в коллекции"
            )
        self._items.remove(item)

    def get_all(self):
        """
        Возвращает список всех квартир в коллекции.

        Returns:
            list: список всех квартир.
        """
        return self._items
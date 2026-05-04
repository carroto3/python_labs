"""
Интерфейсы для классов квартир.
Предметная область: Недвижимость.
"""

from abc import ABC, abstractmethod


class Printable(ABC):
    """
    Интерфейс для объектов, которые можно выводить в разных форматах.
    """

    @abstractmethod
    def to_string(self):
        """
        Возвращает полное строковое представление объекта.

        Returns:
            str: полная информация об объекте
        """
        pass

    @abstractmethod
    def to_short_string(self):
        """
        Возвращает краткое строковое представление объекта.

        Returns:
            str: краткая информация об объекте
        """
        pass


class Comparable(ABC):
    """
    Интерфейс для объектов, которые можно сравнивать.
    """

    @abstractmethod
    def compare_to(self, other):
        """
        Сравнивает текущий объект с другим.

        Args:
            other: объект для сравнения

        Returns:
            int: -1 если текущий меньше, 0 если равны, 1 если текущий больше
        """
        pass
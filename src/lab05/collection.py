"""
Коллекция квартир с поддержкой функций-стратегий.
Предметная область: Недвижимость.
"""


class ApartmentCollection:
    """
    Класс-коллекция для управления множеством квартир.
    Поддерживает сортировку и фильтрацию через функции-стратегии.
    """

    def __init__(self):
        """Инициализирует пустую коллекцию квартир."""
        self._items = []

    def add(self, item):
        """
        Добавляет квартиру в коллекцию.
        
        Args:
            item: объект квартиры для добавления
        """
        self._items.append(item)

    def get_all(self):
        """
        Возвращает список всех квартир в коллекции.
        
        Returns:
            list: список всех квартир
        """
        return self._items

    def sort_by(self, strategy):
        """
        Сортирует коллекцию используя функцию-стратегию.
        
        Args:
            strategy: функция-стратегия для сортировки
            
        Returns:
            list: отсортированный список квартир
        """
        return sorted(self._items, key=strategy)

    def filter_by(self, filter_func):
        """
        Фильтрует коллекцию используя функцию-фильтр.
        
        Args:
            filter_func: функция-фильтр
            
        Returns:
            list: отфильтрованный список квартир
        """
        return list(filter(filter_func, self._items))

    def __len__(self):
        """Возвращает количество квартир в коллекции."""
        return len(self._items)

    def __iter__(self):
        """Возвращает итератор для перебора квартир."""
        return iter(self._items)
"""
Типизированная коллекция с использованием Generic.
Предметная область: Недвижимость.
"""

from typing import TypeVar, Generic, List, Optional


# Определяем переменную типа
T = TypeVar('T')


class TypedCollection(Generic[T]):
    """
    Обобщённая (generic) коллекция для хранения объектов определённого типа.
    
    Использует TypeVar для обеспечения типобезопасности.
    
    Type Parameters:
        T: тип элементов, хранящихся в коллекции
    
    Attributes:
        _items: список элементов типа T
    """

    def __init__(self) -> None:
        """
        Инициализирует пустую типизированную коллекцию.
        """
        self._items: List[T] = []

    def add(self, item: T) -> None:
        """
        Добавляет элемент в коллекцию.
        
        Args:
            item: элемент типа T для добавления
        """
        self._items.append(item)

    def remove(self, item: T) -> None:
        """
        Удаляет элемент из коллекции.
        
        Args:
            item: элемент типа T для удаления
            
        Raises:
            ValueError: если элемент не найден в коллекции
        """
        if item not in self._items:
            raise ValueError("Элемент не найден в коллекции")
        self._items.remove(item)

    def get_all(self) -> List[T]:
        """
        Возвращает список всех элементов в коллекции.
        
        Returns:
            копия списка всех элементов типа T
        """
        return self._items.copy()

    def get_by_index(self, index: int) -> T:
        """
        Возвращает элемент по индексу.
        
        Args:
            index: индекс элемента
            
        Returns:
            элемент типа T по указанному индексу
            
        Raises:
            IndexError: если индекс вне диапазона
        """
        return self._items[index]

    def find(self, predicate) -> Optional[T]:
        """
        Находит первый элемент, удовлетворяющий условию.
        
        Args:
            predicate: функция-предикат для проверки элементов
            
        Returns:
            первый найденный элемент типа T или None
        """
        for item in self._items:
            if predicate(item):
                return item
        return None

    def __len__(self) -> int:
        """
        Возвращает количество элементов в коллекции.
        
        Returns:
            количество элементов
        """
        return len(self._items)

    def __iter__(self):
        """
        Возвращает итератор для перебора элементов.
        
        Returns:
            итератор по элементам коллекции
        """
        return iter(self._items)

    def __str__(self) -> str:
        """
        Возвращает строковое представление коллекции.
        
        Returns:
            строка с информацией о коллекции
        """
        return f"TypedCollection[{type(self).__name__}](size={len(self._items)})"

    def __repr__(self) -> str:
        """
        Возвращает техническое представление коллекции.
        
        Returns:
            строка для отладки
        """
        return f"TypedCollection(items={len(self._items)})"
"""
Модуль бизнес-логики приложения.
Предметная область: Недвижимость.

Содержит класс ApartmentService, который управляет коллекцией
объектов недвижимости и предоставляет все операции для CLI-слоя.
CLI не должен напрямую обращаться к коллекции — только через этот сервис.

Все публичные методы имеют полные аннотации типов и docstring'и.
"""

from typing import Callable, Any, Optional

from models import (
    Apartment,
    ResidentialApartment,
    CommercialApartment,
)
from exceptions import ItemNotFoundError, DuplicateItemError


# ── Типы-алиасы для стратегий ────────────────────────────────────────────

SortStrategy = Callable[[Apartment], Any]
"""Функция-стратегия сортировки: принимает Apartment, возвращает ключ."""

FilterPredicate = Callable[[Apartment], bool]
"""Функция-предикат для фильтрации: принимает Apartment, возвращает bool."""


# ── Сервисный класс ──────────────────────────────────────────────────────

class ApartmentService:
    """
    Сервис для управления коллекцией объектов недвижимости.

    Предоставляет методы для добавления, удаления, поиска,
    фильтрации и сортировки объектов. Содержит всю бизнес-логику
    и не выполняет операций ввода-вывода напрямую.

    Слой бизнес-логики (app.py) изолирован от слоя представления (cli.py):
    CLI вызывает методы сервиса и получает готовые результаты.

    Attributes:
        _items (list[Apartment]): внутренний список объектов недвижимости.
    """

    def __init__(self) -> None:
        """Инициализирует пустой сервис с пустой коллекцией объектов."""
        self._items: list[Apartment] = []

    # ── Базовые операции CRUD ────────────────────────────────────────────

    def add(self, item: Apartment) -> None:
        """
        Добавляет объект недвижимости в коллекцию.

        Выполняет проверку на дубликат по идентификатору перед добавлением.

        Args:
            item: объект Apartment (или производного класса) для добавления.

        Raises:
            TypeError: если передан объект, не являющийся экземпляром Apartment.
            DuplicateItemError: если объект с таким ID уже существует в коллекции.
        """
        if not isinstance(item, Apartment):
            raise TypeError(
                f"Можно добавлять только объекты типа Apartment, "
                f"получен {type(item).__name__}"
            )
        if self.find_by_id(item.id) is not None:
            raise DuplicateItemError(item.id)
        self._items.append(item)

    def remove(self, item_id: str) -> Apartment:
        """
        Удаляет объект недвижимости из коллекции по идентификатору.

        Args:
            item_id: уникальный идентификатор (UUID) объекта для удаления.

        Returns:
            Apartment: удалённый объект.

        Raises:
            ItemNotFoundError: если объект с указанным ID не найден в коллекции.
        """
        item: Optional[Apartment] = self.find_by_id(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        self._items.remove(item)
        return item

    def update_price(self, item_id: str, new_price: float) -> Apartment:
        """
        Обновляет цену аренды объекта недвижимости.

        Args:
            item_id: идентификатор объекта.
            new_price: новая цена аренды в рублях.

        Returns:
            Apartment: обновлённый объект.

        Raises:
            ItemNotFoundError: если объект с указанным ID не найден.
            TypeError, ValueError: при некорректном значении цены (из сеттера).
        """
        item: Optional[Apartment] = self.find_by_id(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        item.price = new_price
        return item

    def update_status(self, item_id: str, new_status: str) -> Apartment:
        """
        Обновляет статус объекта недвижимости.

        Args:
            item_id: идентификатор объекта.
            new_status: новый статус (из списка Apartment.AVAILABLE_STATUSES).

        Returns:
            Apartment: обновлённый объект.

        Raises:
            ItemNotFoundError: если объект с указанным ID не найден.
            TypeError, ValueError: при некорректном статусе (из сеттера).
        """
        item: Optional[Apartment] = self.find_by_id(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        item.status = new_status
        return item

    def get_all(self) -> list[Apartment]:
        """
        Возвращает копию списка всех объектов в коллекции.

        Returns:
            list[Apartment]: копия списка всех объектов недвижимости.
        """
        return self._items.copy()

    def find_by_id(self, item_id: str) -> Optional[Apartment]:
        """
        Находит объект недвижимости по его уникальному идентификатору.

        Args:
            item_id: идентификатор (UUID) для поиска.

        Returns:
            Optional[Apartment]: найденный объект или None, если не найден.
        """
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    # ── Поиск по атрибуту ────────────────────────────────────────────────

    def search_by_address(self, query: str) -> list[Apartment]:
        """
        Ищет объекты по подстроке в адресе (без учёта регистра).

        Args:
            query: поисковый запрос — подстрока, которая должна
                   содержаться в адресе объекта.

        Returns:
            list[Apartment]: список объектов, адрес которых содержит запрос.
                             Пустой список, если ничего не найдено.
        """
        query_lower: str = query.strip().lower()
        if not query_lower:
            return []
        return [
            item for item in self._items
            if query_lower in item.address.lower()
        ]

    def search_by_attribute(self, attribute: str, value: str) -> list[Apartment]:
        """
        Ищет объекты по заданному атрибуту и значению.

        Поддерживаемые атрибуты:
            - 'address'  — поиск по подстроке в адресе.
            - 'status'   — точное совпадение статуса.
            - 'rooms'    — точное совпадение количества комнат.
            - 'type'     — фильтрация по имени класса
                           (Apartment / ResidentialApartment / CommercialApartment).

        Args:
            attribute: имя атрибута для поиска (регистронезависимо).
            value: значение для поиска.

        Returns:
            list[Apartment]: список найденных объектов.

        Raises:
            ValueError: если атрибут не поддерживается или значение некорректно.
        """
        attribute = attribute.strip().lower()
        value = value.strip()

        if attribute == "address":
            return self.search_by_address(value)

        elif attribute == "status":
            value_lower: str = value.lower()
            return [
                item for item in self._items
                if item.status.lower() == value_lower
            ]

        elif attribute == "rooms":
            try:
                rooms_val: int = int(value)
            except ValueError as exc:
                raise ValueError(
                    f"Количество комнат должно быть целым числом, "
                    f"получено: '{value}'"
                ) from exc
            return [
                item for item in self._items
                if item.rooms == rooms_val
            ]

        elif attribute == "type":
            type_map: dict[str, type] = {
                "apartment": Apartment,
                "residential": ResidentialApartment,
                "residentialapartment": ResidentialApartment,
                "commercial": CommercialApartment,
                "commercialapartment": CommercialApartment,
            }
            clean_value: str = value.lower().replace(" ", "")
            target_type: type | None = type_map.get(clean_value)
            if target_type is None:
                raise ValueError(
                    f"Неизвестный тип объекта: '{value}'. "
                    f"Допустимые: apartment, residential, commercial"
                )
            return [
                item for item in self._items
                if type(item) is target_type
            ]

        else:
            raise ValueError(
                f"Неизвестный атрибут: '{attribute}'. "
                f"Допустимые: address, status, rooms, type"
            )

    # ── Фильтрация ───────────────────────────────────────────────────────

    def filter_by_price_range(
        self, min_price: float, max_price: float
    ) -> list[Apartment]:
        """
        Фильтрует объекты по диапазону цен (включительно).

        Args:
            min_price: минимальная цена аренды в рублях.
            max_price: максимальная цена аренды в рублях.

        Returns:
            list[Apartment]: объекты, цена которых попадает в диапазон.

        Raises:
            ValueError: если min_price > max_price.
        """
        if min_price > max_price:
            raise ValueError(
                f"Минимальная цена ({min_price:,.0f}) не может быть больше "
                f"максимальной ({max_price:,.0f})"
            )
        return [
            item for item in self._items
            if min_price <= item.price <= max_price
        ]

    def filter_by_area_range(
        self, min_area: float, max_area: float
    ) -> list[Apartment]:
        """
        Фильтрует объекты по диапазону площади (включительно).

        Args:
            min_area: минимальная площадь в м².
            max_area: максимальная площадь в м².

        Returns:
            list[Apartment]: объекты, площадь которых попадает в диапазон.

        Raises:
            ValueError: если min_area > max_area.
        """
        if min_area > max_area:
            raise ValueError(
                f"Минимальная площадь ({min_area:.1f}) не может быть больше "
                f"максимальной ({max_area:.1f})"
            )
        return [
            item for item in self._items
            if min_area <= item.area <= max_area
        ]

    def filter_by_status(self, status: str) -> list[Apartment]:
        """
        Фильтрует объекты по статусу (точное совпадение, без учёта регистра).

        Args:
            status: статус для фильтрации (available, rented, reserved).

        Returns:
            list[Apartment]: объекты с указанным статусом.
        """
        status_lower: str = status.strip().lower()
        return [
            item for item in self._items
            if item.status.lower() == status_lower
        ]

    def filter_by_type(self, object_type: str) -> list[Apartment]:
        """
        Фильтрует объекты по типу: только жилые или только коммерческие.

        Args:
            object_type: строка, определяющая тип:
                         'residential' или 'жилая' — только жилые квартиры.
                         'commercial' или 'коммерческая' — только коммерческие.

        Returns:
            list[Apartment]: объекты указанного типа.

        Raises:
            ValueError: если передан неизвестный тип.
        """
        object_type = object_type.strip().lower()
        if object_type in ("residential", "жилая"):
            return [
                item for item in self._items
                if isinstance(item, ResidentialApartment)
            ]
        elif object_type in ("commercial", "коммерческая"):
            return [
                item for item in self._items
                if isinstance(item, CommercialApartment)
            ]
        else:
            raise ValueError(
                f"Неизвестный тип: '{object_type}'. "
                f"Допустимые: residential (жилая), commercial (коммерческая)"
            )

    def filter_by(self, predicate: FilterPredicate) -> list[Apartment]:
        """
        Фильтрует объекты по произвольному пользовательскому предикату.

        Args:
            predicate: функция, принимающая Apartment и возвращающая bool.
                       True означает, что объект проходит фильтр.

        Returns:
            list[Apartment]: объекты, удовлетворяющие предикату.
        """
        return [item for item in self._items if predicate(item)]

    # ── Сортировка ───────────────────────────────────────────────────────

    def sort_by(
        self, strategy: SortStrategy, reverse: bool = False
    ) -> list[Apartment]:
        """
        Сортирует объекты по заданной стратегии (функции-ключу).

        Args:
            strategy: функция, извлекающая ключ сортировки из объекта Apartment.
            reverse: если True — сортировка по убыванию.

        Returns:
            list[Apartment]: новый отсортированный список (исходная коллекция
                             не изменяется).
        """
        return sorted(self._items, key=strategy, reverse=reverse)

    def sort_by_address(self, reverse: bool = False) -> list[Apartment]:
        """
        Сортирует объекты по адресу (названию) в алфавитном порядке.

        Args:
            reverse: если True — в обратном алфавитном порядке (Z → A).

        Returns:
            list[Apartment]: отсортированный список объектов.
        """
        return self.sort_by(
            lambda item: item.address.lower(), reverse=reverse
        )

    def sort_by_price(self, reverse: bool = False) -> list[Apartment]:
        """
        Сортирует объекты по цене аренды.

        Args:
            reverse: если True — по убыванию цены (от дорогих к дешёвым).

        Returns:
            list[Apartment]: отсортированный список объектов.
        """
        return self.sort_by(lambda item: item.price, reverse=reverse)

    def sort_by_date_added(self, reverse: bool = False) -> list[Apartment]:
        """
        Сортирует объекты по дате добавления.

        Args:
            reverse: если True — сначала новые (по убыванию даты).

        Returns:
            list[Apartment]: отсортированный список объектов.
        """
        return self.sort_by(lambda item: item.date_added, reverse=reverse)

    def sort_by_area(self, reverse: bool = False) -> list[Apartment]:
        """
        Сортирует объекты по площади.

        Args:
            reverse: если True — по убыванию площади (от больших к маленьким).

        Returns:
            list[Apartment]: отсортированный список объектов.
        """
        return self.sort_by(lambda item: item.area, reverse=reverse)

    # ── Статистика ───────────────────────────────────────────────────────

    def count(self) -> int:
        """
        Возвращает количество объектов в коллекции.

        Returns:
            int: количество объектов.
        """
        return len(self._items)

    def get_statistics(self) -> dict[str, Any]:
        """
        Возвращает статистическую сводку по коллекции.

        Включает общее количество, среднюю/мин/макс цену,
        среднюю площадь, распределение по статусам и типам объектов.

        Returns:
            dict[str, Any]: словарь со статистическими показателями.
            Если коллекция пуста, возвращает нулевые значения.
        """
        if not self._items:
            return {
                "total": 0,
                "avg_price": 0.0,
                "avg_area": 0.0,
                "min_price": 0.0,
                "max_price": 0.0,
                "statuses": {},
                "types": {},
            }

        prices: list[float] = [item.price for item in self._items]
        areas: list[float] = [item.area for item in self._items]

        status_counts: dict[str, int] = {}
        type_counts: dict[str, int] = {}

        for item in self._items:
            status_counts[item.status] = (
                status_counts.get(item.status, 0) + 1
            )
            type_name: str = type(item).__name__
            type_counts[type_name] = (
                type_counts.get(type_name, 0) + 1
            )

        return {
            "total": len(self._items),
            "avg_price": sum(prices) / len(prices),
            "avg_area": sum(areas) / len(areas),
            "min_price": min(prices),
            "max_price": max(prices),
            "statuses": status_counts,
            "types": type_counts,
        }

    # ── Работа с данными коллекции ──────────────────────────────────────

    def set_items(self, items: list[Apartment]) -> None:
        """
        Заменяет всю коллекцию новым списком объектов.

        Используется при загрузке данных из файла.

        Args:
            items: новый список объектов Apartment для замены коллекции.
        """
        self._items = items.copy()

    def clear(self) -> None:
        """Очищает коллекцию, удаляя все объекты без возможности восстановления."""
        self._items.clear()

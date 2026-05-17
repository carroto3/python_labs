"""
Модуль бизнес-логики приложения «Недвижимость».
Управляет коллекцией объектов недвижимости:
добавление, удаление, поиск, фильтрация.
CLI не должен обращаться к коллекции напрямую — только через этот модуль.
"""

from typing import List, Optional, Callable, Any

from models import (
    Apartment,
    ResidentialApartment,
    CommercialApartment,
    Printable,
    Comparable,
)
from exceptions import (
    ItemNotFoundError,
    DuplicateItemError,
    ValidationError,
    StorageError,
)
from storage import Storage


# ------------------------------------------------------------------
# Демонстрационные данные (для первоначальной загрузки)
# ------------------------------------------------------------------

_DEMO_APARTMENTS: List[Apartment] = [
    Apartment(1, "ул. Ленина, д. 10, кв. 45", 55.0, 4500000.0, 2, "доступна"),
    Apartment(2, "пр. Мира, д. 25, кв. 12", 72.0, 6800000.0, 3, "продана"),
    Apartment(3, "ул. Пушкина, д. 5, кв. 88", 38.0, 3200000.0, 1, "доступна"),
    ResidentialApartment(4, "ул. Садовая, д. 15, кв. 32", 68.0, 5200000.0, 3, True, 5, "доступна"),
    ResidentialApartment(5, "ул. Цветочная, д. 8, кв. 7", 48.0, 3800000.0, 2, False, 2, "забронирована"),
    CommercialApartment(6, "ул. Деловая, д. 3, оф. 101", 120.0, 9500000.0, 5, "офис", True, "доступна"),
    CommercialApartment(7, "пр. Торговый, д. 12, пом. 5", 85.0, 6100000.0, 3, "магазин", False, "доступна"),
]

# Атрибуты, доступные для поиска
_SEARCHABLE_ATTRS: List[str] = [
    "address", "area", "price", "rooms", "status",
    "has_balcony", "floor", "business_type", "has_parking",
]

# Отображение кода типа в класс
_TYPE_CLASSES = {
    "1": Apartment,
    "2": ResidentialApartment,
    "3": CommercialApartment,
}


class ApartmentManager:
    """Управление коллекцией объектов недвижимости.

    Предоставляет CRUD-операции, поиск, фильтрацию,
    сохранение и загрузку данных.

    Attributes:
        items (List[Apartment]): коллекция объектов.
    """

    def __init__(self, storage: Optional[Storage] = None) -> None:
        """Инициализация менеджера.

        Args:
            storage (Storage, optional): объект хранилища.
        """
        self._items: List[Apartment] = []
        self._next_id: int = 1
        self._storage = storage

    # ------------------------------------------------------------------
    # Свойства
    # ------------------------------------------------------------------

    @property
    def items(self) -> List[Apartment]:
        """Возвращает копию списка (безопасное чтение)."""
        return list(self._items)

    @property
    def count(self) -> int:
        """Количество объектов в коллекции."""
        return len(self._items)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_apartment(
        self,
        type_code: str,
        address: str,
        area: float,
        price: float,
        rooms: int,
        status: str = "доступна",
        **extra_fields,
    ) -> Apartment:
        """Добавляет новый объект недвижимости.

        Args:
            type_code (str): код типа ("1" = Apartment, "2" = Residential, "3" = Commercial).
            address (str): адрес.
            area (float): площадь.
            price (float): цена.
            rooms (int): количество комнат.
            status (str): статус.
            **extra_fields: доп. поля для Residential/Commercial.

        Returns:
            Apartment: созданный объект.

        Raises:
            ValidationError: при некорректных данных.
            DuplicateItemError: при дублировании ID (не должно возникать).
        """
        cls = _TYPE_CLASSES.get(type_code, Apartment)
        item_id = self._next_id
        self._next_id += 1

        try:
            item = cls(
                apartment_id=item_id,
                address=address,
                area=area,
                price=price,
                rooms=rooms,
                status=status,
                **extra_fields,
            )
        except (ValueError, TypeError) as e:
            self._next_id -= 1  # откат ID
            raise ValidationError(message=str(e)) from e

        self._items.append(item)
        return item

    def get_all(self) -> List[Apartment]:
        """Возвращает все объекты."""
        return self.items

    def get_by_id(self, item_id: int) -> Apartment:
        """Находит объект по ID.

        Raises:
            ItemNotFoundError: если не найден.
        """
        for item in self._items:
            if item.id == item_id:
                return item
        raise ItemNotFoundError(item_id)

    def remove_by_id(self, item_id: int) -> Apartment:
        """Удаляет объект по ID.

        Raises:
            ItemNotFoundError: если не найден.
        """
        for i, item in enumerate(self._items):
            if item.id == item_id:
                return self._items.pop(i)
        raise ItemNotFoundError(item_id)

    # ------------------------------------------------------------------
    # Поиск (ЛР5)
    # ------------------------------------------------------------------

    def find_by_attribute(self, attr: str, value: str) -> List[Apartment]:
        """Поиск объектов по значению атрибута (без учёта регистра).

        Args:
            attr (str): имя атрибута.
            value (str): искомое значение.

        Returns:
            List[Apartment]: найденные объекты.

        Raises:
            ValidationError: если атрибут не поддерживается.
        """
        if attr not in _SEARCHABLE_ATTRS:
            raise ValidationError(
                attr,
                f"Поиск по атрибуту '{attr}' не поддерживается. "
                f"Доступные: {', '.join(_SEARCHABLE_ATTRS)}",
            )
        results = []
        for item in self._items:
            if hasattr(item, attr):
                actual = getattr(item, attr)
                if str(actual).lower() == value.lower():
                    results.append(item)
        return results

    def find_by_predicate(self, predicate: Callable[[Apartment], bool]) -> List[Apartment]:
        """Поиск по пользовательскому условию-предикату.

        Args:
            predicate (Callable): функция, принимающая Apartment, возвращающая bool.

        Returns:
            List[Apartment]: отфильтрованные объекты.
        """
        return [item for item in self._items if predicate(item)]

    # ------------------------------------------------------------------
    # Фильтрация (ЛР5)
    # ------------------------------------------------------------------

    def filter_by_price_range(self, min_price: float, max_price: float) -> List[Apartment]:
        """Фильтрация по диапазону цен."""
        return self.find_by_predicate(
            lambda a: min_price <= a.price <= max_price
        )

    def filter_by_area_range(self, min_area: float, max_area: float) -> List[Apartment]:
        """Фильтрация по диапазону площади."""
        return self.find_by_predicate(
            lambda a: min_area <= a.area <= max_area
        )

    def filter_by_rooms(self, rooms: int) -> List[Apartment]:
        """Фильтрация по количеству комнат."""
        return self.find_by_predicate(lambda a: a.rooms == rooms)

    def filter_by_status(self, status: str) -> List[Apartment]:
        """Фильтрация по статусу."""
        return self.find_by_predicate(
            lambda a: a.status.lower() == status.lower()
        )

    def filter_by_type(self, type_class: type) -> List[Apartment]:
        """Фильтрация по типу объекта (Apartment / Residential / Commercial)."""
        return self.find_by_predicate(lambda a: isinstance(a, type_class))

    # ------------------------------------------------------------------
    # Сохранение / загрузка
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Сохраняет коллекцию в хранилище.

        Raises:
            StorageError: если хранилище не настроено или ошибка записи.
        """
        if self._storage is None:
            raise StorageError(message="Хранилище не настроено.")
        self._storage.save(self._items)

    def load(self) -> None:
        """Загружает коллекцию из хранилища.

        Если файл пуст или отсутствует — загружаются демо-данные.
        """
        if self._storage is None:
            raise StorageError(message="Хранилище не настроено.")
        loaded = self._storage.load()
        if loaded:
            self._items = loaded
            self._next_id = max(item.id for item in self._items) + 1
        else:
            self._load_demo()

    def _load_demo(self) -> None:
        """Загружает демонстрационные данные."""
        self._items = list(_DEMO_APARTMENTS)
        self._next_id = max(item.id for item in self._items) + 1 if self._items else 1

    def reset_to_demo(self) -> None:
        """Сбрасывает коллекцию к демо-данным."""
        self._load_demo()

    # ------------------------------------------------------------------
    # Утилиты для CLI
    # ------------------------------------------------------------------

    @staticmethod
    def get_searchable_attributes() -> List[str]:
        """Возвращает список атрибутов для поиска."""
        return list(_SEARCHABLE_ATTRS)

    @staticmethod
    def get_type_options() -> dict:
        """Возвращает доступные типы объектов."""
        return {
            "1": ("Обычная квартира", Apartment),
            "2": ("Жилая квартира", ResidentialApartment),
            "3": ("Коммерческая недвижимость", CommercialApartment),
        }

    @staticmethod
    def validate_float(value: Any, field_name: str = "value") -> float:
        """Валидация и преобразование в float."""
        try:
            result = float(value)
        except (ValueError, TypeError) as e:
            raise ValidationError(field_name, f"Значение должно быть числом.") from e
        return result

    @staticmethod
    def validate_int(value: Any, field_name: str = "value") -> int:
        """Валидация и преобразование в int."""
        try:
            result = int(value)
        except (ValueError, TypeError) as e:
            raise ValidationError(field_name, f"Значение должно быть целым числом.") from e
        return result

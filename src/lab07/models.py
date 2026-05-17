"""
Модуль моделей предметной области «Недвижимость» (ЛР1–ЛР6).
Содержит базовый класс Apartment и его наследников,
а также абстрактные интерфейсы Printable и Comparable.
Иерархия сохранена без изменений относительно ЛР1–ЛР6.
"""

from abc import ABC, abstractmethod
from typing import ClassVar, Tuple


# ===================================================================
# Интерфейсы (ЛР4)
# ===================================================================

class Printable(ABC):
    """Абстрактный класс: объект, который можно вывести на экран."""

    @abstractmethod
    def to_string(self) -> str:
        """Полное строковое представление объекта."""
        pass

    @abstractmethod
    def to_short_string(self) -> str:
        """Краткое строковое представление объекта."""
        pass


class Comparable(ABC):
    """Абстрактный класс: объект, который можно сравнивать."""

    @abstractmethod
    def compare_to(self, other: "Comparable") -> int:
        """Сравнивает текущий объект с другим.

        Returns:
            int: отрицательное, если self < other;
                 0, если равны;
                 положительное, если self > other.
        """
        pass


# ===================================================================
# Базовый класс Apartment (ЛР1, ЛР4)
# ===================================================================

class Apartment(Printable, Comparable):
    """Класс, представляющий квартиру в системе недвижимости.

    Атрибуты класса:
        AVAILABLE_STATUSES (tuple): допустимые статусы квартиры.
        _total_count (int): общее количество созданных объектов.

    Атрибуты экземпляра:
        _address  (str)   — адрес квартиры
        _area     (float) — площадь в кв.м.
        _price    (float) — цена в рублях
        _rooms    (int)   — количество комнат
        _status   (str)   — статус (по умолчанию "доступна")
    """

    AVAILABLE_STATUSES: ClassVar[Tuple[str, ...]] = (
        "доступна",
        "продана",
        "забронирована",
    )
    _total_count: ClassVar[int] = 0

    def __init__(
        self,
        apartment_id: int,
        address: str,
        area: float,
        price: float,
        rooms: int,
        status: str = "доступна",
    ) -> None:
        """Инициализация объекта квартиры с валидацией.

        Args:
            apartment_id (int): уникальный идентификатор.
            address (str): адрес квартиры.
            area (float): площадь в кв.м.
            price (float): цена в рублях.
            rooms (int): количество комнат.
            status (str): статус.
        """
        self._id = apartment_id
        self._address = self._validate_address(address)
        self._area = self._validate_area(area)
        self._price = self._validate_price(price)
        self._rooms = self._validate_rooms(rooms)
        self._status = (
            status if status in self.AVAILABLE_STATUSES else "доступна"
        )
        Apartment._total_count += 1

    # ------------------------------------------------------------------
    # Валидация
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_address(address: str) -> str:
        """Валидация адреса."""
        if not address or not address.strip():
            raise ValueError("Адрес не может быть пустым.")
        return address.strip()

    @staticmethod
    def _validate_area(area: float) -> float:
        """Валидация площади."""
        if area <= 0:
            raise ValueError("Площадь должна быть положительной.")
        if area > 10000:
            raise ValueError("Площадь не может превышать 10 000 кв.м.")
        return float(area)

    @staticmethod
    def _validate_price(price: float) -> float:
        """Валидация цены."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной.")
        return float(price)

    @staticmethod
    def _validate_rooms(rooms: int) -> int:
        """Валидация количества комнат."""
        if rooms <= 0:
            raise ValueError("Количество комнат должно быть положительным.")
        if rooms > 100:
            raise ValueError("Количество комнат не может превышать 100.")
        return int(rooms)

    # ------------------------------------------------------------------
    # Свойства (инкапсуляция)
    # ------------------------------------------------------------------

    @property
    def id(self) -> int:
        """Уникальный идентификатор."""
        return self._id

    @property
    def address(self) -> str:
        """Адрес квартиры (только чтение)."""
        return self._address

    @property
    def area(self) -> float:
        """Площадь в кв.м. (только чтение)."""
        return self._area

    @property
    def rooms(self) -> int:
        """Количество комнат (только чтение)."""
        return self._rooms

    @property
    def price(self) -> float:
        """Цена в рублях."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Изменение цены с валидацией."""
        self._price = self._validate_price(new_price)

    @property
    def status(self) -> str:
        """Статус квартиры."""
        return self._status

    @status.setter
    def status(self, new_status: str) -> None:
        """Изменение статуса с проверкой."""
        if new_status not in self.AVAILABLE_STATUSES:
            raise ValueError(
                f"Недопустимый статус: '{new_status}'. "
                f"Допустимые значения: {self.AVAILABLE_STATUSES}"
            )
        self._status = new_status

    # ------------------------------------------------------------------
    # Бизнес-методы
    # ------------------------------------------------------------------

    def price_per_sqm(self) -> float:
        """Цена за квадратный метр."""
        return self._price / self._area if self._area > 0 else 0.0

    def monthly_cost_with_tax(self, tax_rate: float = 0.13) -> float:
        """Ежемесячный платёж с учётом налога (упрощённо).

        Args:
            tax_rate (float): налоговая ставка (по умолчанию 13%).

        Returns:
            float: цена / 12 + налог.
        """
        monthly = self._price / 12.0
        return monthly * (1.0 + tax_rate)

    # ------------------------------------------------------------------
    # Реализация интерфейсов
    # ------------------------------------------------------------------

    def to_string(self) -> str:
        """Полное строковое представление (Printable)."""
        return (
            f"Apartment [ID={self._id}] {self._address}, "
            f"{self._area:.1f} кв.м, {self._rooms} комн., "
            f"{self._price:,.0f} руб., статус: {self._status}"
        )

    def to_short_string(self) -> str:
        """Краткое строковое представление (Printable)."""
        return (
            f"[{self._id}] {self._address[:30]}, "
            f"{self._rooms}к, {self._price:,.0f}р"
        )

    def compare_to(self, other: "Apartment") -> int:
        """Сравнение по цене (Comparable)."""
        if not isinstance(other, Apartment):
            raise TypeError("Сравнение возможно только с объектами Apartment.")
        if self._price < other._price:
            return -1
        if self._price > other._price:
            return 1
        return 0

    # ------------------------------------------------------------------
    # Магические методы
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return (
            f"Apartment(id={self._id}, address='{self._address}', "
            f"area={self._area}, price={self._price}, rooms={self._rooms})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Apartment):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __lt__(self, other: "Apartment") -> bool:
        return self.compare_to(other) < 0

    def __le__(self, other: "Apartment") -> bool:
        return self.compare_to(other) <= 0

    def __gt__(self, other: "Apartment") -> bool:
        return self.compare_to(other) > 0

    def __ge__(self, other: "Apartment") -> bool:
        return self.compare_to(other) >= 0

    # ------------------------------------------------------------------
    # Сериализация
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Сериализация объекта в словарь."""
        return {
            "type": self.__class__.__name__,
            "apartment_id": self._id,
            "address": self._address,
            "area": self._area,
            "price": self._price,
            "rooms": self._rooms,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Apartment":
        """Десериализация объекта из словаря."""
        clean = {k: v for k, v in data.items() if k != "type"}
        # Если ключ "id" вместо "apartment_id" — переименовываем
        if "id" in clean and "apartment_id" not in clean:
            clean["apartment_id"] = clean.pop("id")
        return cls(**clean)

    @classmethod
    def get_total_count(cls) -> int:
        """Возвращает общее количество созданных объектов."""
        return cls._total_count


# ===================================================================
# Наследник: ResidentialApartment (ЛР3)
# ===================================================================

class ResidentialApartment(Apartment):
    """Класс жилой квартиры. Наследует Apartment.

    Дополнительные атрибуты:
        has_balcony (bool): наличие балкона.
        floor (int): этаж.
    """

    def __init__(
        self,
        apartment_id: int,
        address: str,
        area: float,
        price: float,
        rooms: int,
        has_balcony: bool = False,
        floor: int = 1,
        status: str = "доступна",
    ) -> None:
        """Инициализация жилой квартиры."""
        super().__init__(apartment_id, address, area, price, rooms, status)
        self.has_balcony = has_balcony
        self.floor = self._validate_floor(floor)

    @staticmethod
    def _validate_floor(floor: int) -> int:
        """Валидация этажа."""
        if floor < 1:
            raise ValueError("Этаж не может быть меньше 1.")
        if floor > 200:
            raise ValueError("Этаж не может превышать 200.")
        return int(floor)

    def is_suitable_for_family(self, min_rooms: int = 2) -> bool:
        """Проверяет, подходит ли квартира для семьи.

        Args:
            min_rooms (int): минимальное количество комнат.

        Returns:
            bool: True, если комнат достаточно.
        """
        return self.rooms >= min_rooms

    # ------------------------------------------------------------------
    # Реализация интерфейсов
    # ------------------------------------------------------------------

    def to_string(self) -> str:
        """Полное строковое представление."""
        base = super().to_string()
        balcony = "есть балкон" if self.has_balcony else "без балкона"
        return f"{base} | {self.floor} эт., {balcony}"

    def to_short_string(self) -> str:
        """Краткое строковое представление."""
        base = super().to_short_string()
        return f"{base} | жилая, {self.floor}эт"

    def compare_to(self, other: "Apartment") -> int:
        """Сравнение: сначала по цене, при равенстве — по площади."""
        base = super().compare_to(other)
        if base != 0:
            return base
        if self.area < other.area:
            return -1
        if self.area > other.area:
            return 1
        return 0

    # ------------------------------------------------------------------
    # Сериализация
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Сериализация с дополнительными полями."""
        data = super().to_dict()
        data["has_balcony"] = self.has_balcony
        data["floor"] = self.floor
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "ResidentialApartment":
        """Десериализация."""
        clean = {k: v for k, v in data.items() if k != "type"}
        if "id" in clean and "apartment_id" not in clean:
            clean["apartment_id"] = clean.pop("id")
        return cls(**clean)


# ===================================================================
# Наследник: CommercialApartment (ЛР3)
# ===================================================================

class CommercialApartment(Apartment):
    """Класс коммерческой недвижимости. Наследует Apartment.

    Дополнительные атрибуты:
        business_type (str): тип бизнеса.
        has_parking (bool): наличие парковки.
    """

    VALID_BUSINESS_TYPES: ClassVar[Tuple[str, ...]] = (
        "офис",
        "склад",
        "магазин",
        "салон",
        "кафе",
    )

    def __init__(
        self,
        apartment_id: int,
        address: str,
        area: float,
        price: float,
        rooms: int,
        business_type: str = "офис",
        has_parking: bool = False,
        status: str = "доступна",
    ) -> None:
        """Инициализация коммерческой недвижимости."""
        super().__init__(apartment_id, address, area, price, rooms, status)
        self.business_type = (
            business_type
            if business_type in self.VALID_BUSINESS_TYPES
            else "офис"
        )
        self.has_parking = has_parking

    def calculate_business_cost(self, clients_per_day: int = 0) -> float:
        """Примерный расчёт стоимости для бизнеса.

        Args:
            clients_per_day (int): ориентировочное количество клиентов в день.

        Returns:
            float: оценочная стоимость.
        """
        base = self.price_per_sqm() * 10.0
        return base + clients_per_day * 50.0

    # ------------------------------------------------------------------
    # Реализация интерфейсов
    # ------------------------------------------------------------------

    def to_string(self) -> str:
        """Полное строковое представление."""
        base = super().to_string()
        parking = "с парковкой" if self.has_parking else "без парковки"
        return f"{base} | тип: {self.business_type}, {parking}"

    def to_short_string(self) -> str:
        """Краткое строковое представление."""
        base = super().to_short_string()
        return f"{base} | {self.business_type}"

    def compare_to(self, other: "Apartment") -> int:
        """Сравнение: по цене, затем по площади."""
        base = super().compare_to(other)
        if base != 0:
            return base
        if self.area < other.area:
            return -1
        if self.area > other.area:
            return 1
        return 0

    # ------------------------------------------------------------------
    # Сериализация
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Сериализация с дополнительными полями."""
        data = super().to_dict()
        data["business_type"] = self.business_type
        data["has_parking"] = self.has_parking
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "CommercialApartment":
        """Десериализация."""
        clean = {k: v for k, v in data.items() if k != "type"}
        if "id" in clean and "apartment_id" not in clean:
            clean["apartment_id"] = clean.pop("id")
        return cls(**clean)


# Отображение типа в класс (для полиморфной десериализации)
_TYPE_MAP = {
    "Apartment": Apartment,
    "ResidentialApartment": ResidentialApartment,
    "CommercialApartment": CommercialApartment,
}


def create_apartment_from_dict(data: dict) -> Apartment:
    """Создаёт объект нужного типа по словарю (полиморфная десериализация).

    Args:
        data (dict): словарь с полем 'type'.

    Returns:
        Apartment: объект соответствующего подкласса.
    """
    type_name = data.get("type", "Apartment")
    cls = _TYPE_MAP.get(type_name, Apartment)
    return cls.from_dict(data)

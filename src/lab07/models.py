"""
Модуль классов предметной области.
Предметная область: Недвижимость.

Содержит базовый класс Apartment и производные классы
ResidentialApartment и CommercialApartment.
Реализует интерфейсы Printable и Comparable.
Включает полную валидацию, свойства, бизнес-методы,
магические методы и сериализацию в словарь.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from uuid import uuid4


# ══════════════════════════════════════════════════════════════════════════
# ИНТЕРФЕЙСЫ
# ══════════════════════════════════════════════════════════════════════════

class Printable(ABC):
    """Интерфейс для объектов, поддерживающих форматированный вывод."""

    @abstractmethod
    def to_string(self) -> str:
        """
        Возвращает полное строковое представление объекта.

        Returns:
            str: полная информация об объекте.
        """
        ...

    @abstractmethod
    def to_short_string(self) -> str:
        """
        Возвращает краткое строковое представление объекта.

        Returns:
            str: краткая информация об объекте.
        """
        ...


class Comparable(ABC):
    """Интерфейс для объектов, поддерживающих сравнение."""

    @abstractmethod
    def compare_to(self, other: Any) -> int:
        """
        Сравнивает текущий объект с другим.

        Args:
            other: объект для сравнения.

        Returns:
            int: -1 если текущий меньше, 0 если равны, 1 если текущий больше.
        """
        ...


# ══════════════════════════════════════════════════════════════════════════
# БАЗОВЫЙ КЛАСС
# ══════════════════════════════════════════════════════════════════════════

class Apartment(Printable, Comparable):
    """
    Базовый класс, представляющий объект недвижимости.

    Атрибуты класса:
        AVAILABLE_STATUSES (tuple[str, ...]): допустимые статусы объекта.
        _total_count (int): общее количество созданных объектов.

    Атрибуты экземпляра:
        _id (str): уникальный идентификатор объекта (UUID).
        _address (str): адрес объекта.
        _area (float): площадь в м².
        _price (float): цена аренды в месяц (руб.).
        _rooms (int): количество комнат.
        _date_added (str): дата добавления в формате ISO 8601.
        _status (str): текущий статус объекта.
    """

    # ── Атрибуты класса ───────────────────────────────────────────────────
    AVAILABLE_STATUSES: tuple[str, ...] = ("available", "rented", "reserved")
    _total_count: int = 0

    # ── Конструктор ───────────────────────────────────────────────────────
    def __init__(
        self,
        address: str,
        area: float,
        price: float,
        rooms: int,
        status: str = "available",
    ) -> None:
        """
        Инициализация объекта недвижимости с проверкой входных данных.

        Args:
            address: адрес объекта (непустая строка, мин. 5 символов).
            area: общая площадь в м² (от 1 до 10 000).
            price: ежемесячная цена аренды в руб. (от 0 до 1 000 000).
            rooms: количество комнат (от 1 до 20).
            status: статус объекта, по умолчанию "available".

        Raises:
            TypeError: если тип аргумента не соответствует ожидаемому.
            ValueError: если значение аргумента вне допустимого диапазона.
        """
        self._id: str = str(uuid4())
        self._address: str = self._validate_address(address)
        self._area: float = self._validate_area(area)
        self._price: float = self._validate_price(price)
        self._rooms: int = self._validate_rooms(rooms)
        self._date_added: str = datetime.now().isoformat()
        self._status: str = self._validate_status(status)

        Apartment._total_count += 1

    # ── Валидация (внутренние статические методы) ─────────────────────────
    @staticmethod
    def _validate_address(address: str) -> str:
        """
        Проверяет корректность адреса.

        Raises:
            TypeError: если address не строка.
            ValueError: если адрес пустой или короче 5 символов.
        """
        if not isinstance(address, str):
            raise TypeError(
                f"Адрес должен быть строкой, "
                f"получен {type(address).__name__}"
            )
        address = address.strip()
        if len(address) == 0:
            raise ValueError("Адрес не может быть пустой строкой")
        if len(address) < 5:
            raise ValueError(
                f"Адрес слишком короткий (минимум 5 символов): '{address}'"
            )
        return address

    @staticmethod
    def _validate_area(area: float) -> float:
        """
        Проверяет корректность площади.

        Raises:
            TypeError: если area не число.
            ValueError: если площадь вне диапазона (0, 10 000].
        """
        if not isinstance(area, (int, float)):
            raise TypeError(
                f"Площадь должна быть числом, "
                f"получен {type(area).__name__}"
            )
        area = float(area)
        if area <= 0:
            raise ValueError(
                f"Площадь должна быть положительной, получено: {area}"
            )
        if area > 10_000:
            raise ValueError(
                f"Площадь слишком большая (максимум 10 000 м²): {area}"
            )
        return area

    @staticmethod
    def _validate_price(price: float) -> float:
        """
        Проверяет корректность цены аренды.

        Raises:
            TypeError: если price не число.
            ValueError: если цена вне диапазона [0, 1 000 000].
        """
        if not isinstance(price, (int, float)):
            raise TypeError(
                f"Цена должна быть числом, "
                f"получен {type(price).__name__}"
            )
        price = float(price)
        if price < 0:
            raise ValueError(
                f"Цена не может быть отрицательной: {price}"
            )
        if price > 1_000_000:
            raise ValueError(
                f"Цена слишком высокая (максимум 1 000 000 руб.): {price}"
            )
        return price

    @staticmethod
    def _validate_rooms(rooms: int) -> int:
        """
        Проверяет корректность количества комнат.

        Raises:
            TypeError: если rooms не целое число.
            ValueError: если количество вне диапазона [1, 20].
        """
        if not isinstance(rooms, int):
            raise TypeError(
                f"Количество комнат должно быть целым числом, "
                f"получен {type(rooms).__name__}"
            )
        if rooms < 1:
            raise ValueError(
                f"Количество комнат не менее 1, получено: {rooms}"
            )
        if rooms > 20:
            raise ValueError(
                f"Количество комнат не более 20, получено: {rooms}"
            )
        return rooms

    @staticmethod
    def _validate_status(status: str) -> str:
        """
        Проверяет корректность статуса.

        Raises:
            TypeError: если status не строка.
            ValueError: если статус не входит в список допустимых.
        """
        if not isinstance(status, str):
            raise TypeError(
                f"Статус должен быть строкой, "
                f"получен {type(status).__name__}"
            )
        status = status.strip().lower()
        if status not in Apartment.AVAILABLE_STATUSES:
            raise ValueError(
                f"Недопустимый статус '{status}'. "
                f"Допустимые: {', '.join(Apartment.AVAILABLE_STATUSES)}"
            )
        return status

    # ── Свойства (только чтение) ──────────────────────────────────────────
    @property
    def id(self) -> str:
        """Уникальный идентификатор объекта (только чтение)."""
        return self._id

    @property
    def address(self) -> str:
        """Адрес объекта (только чтение)."""
        return self._address

    @property
    def area(self) -> float:
        """Площадь в м² (только чтение)."""
        return self._area

    @property
    def rooms(self) -> int:
        """Количество комнат (только чтение)."""
        return self._rooms

    @property
    def date_added(self) -> str:
        """Дата добавления в формате ISO 8601 (только чтение)."""
        return self._date_added

    # ── Свойства с сеттерами ──────────────────────────────────────────────
    @property
    def price(self) -> float:
        """Цена аренды в месяц, руб."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """
        Устанавливает новую цену аренды с валидацией.

        Args:
            new_price: новая цена аренды в руб.

        Raises:
            TypeError: если тип не число.
            ValueError: если цена вне допустимого диапазона.
        """
        self._price = self._validate_price(new_price)

    @property
    def status(self) -> str:
        """Текущий статус объекта."""
        return self._status

    @status.setter
    def status(self, new_status: str) -> None:
        """
        Устанавливает новый статус с валидацией.

        Args:
            new_status: новый статус объекта.

        Raises:
            TypeError: если тип не строка.
            ValueError: если статус недопустим.
        """
        self._status = self._validate_status(new_status)

    # ── Бизнес-методы ─────────────────────────────────────────────────────
    def price_per_sqm(self) -> float:
        """
        Рассчитывает цену аренды за 1 м².

        Returns:
            float: стоимость аренды за 1 м² в месяц (руб./м²).
        """
        return self._price / self._area

    def monthly_cost_with_tax(self, tax_rate: float = 0.13) -> float:
        """
        Рассчитывает ежемесячные расходы с учётом налога.

        Args:
            tax_rate: ставка налога в диапазоне [0.0, 1.0],
                      по умолчанию 13% (0.13).

        Returns:
            float: цена аренды с учётом налога.

        Raises:
            TypeError: если tax_rate не число.
            ValueError: если ставка вне диапазона [0.0, 1.0].
        """
        if not isinstance(tax_rate, (int, float)):
            raise TypeError(
                f"Ставка налога должна быть числом, "
                f"получен {type(tax_rate).__name__}"
            )
        if not (0.0 <= tax_rate <= 1.0):
            raise ValueError(
                f"Ставка налога должна быть в диапазоне [0, 1], "
                f"получено: {tax_rate}"
            )
        return self._price * (1 + tax_rate)

    # ── Реализация интерфейса Printable ───────────────────────────────────
    def to_string(self) -> str:
        """
        Возвращает полное строковое представление объекта.
        Используется для детального вывода.
        """
        return (
            f"Квартира\n"
            f"  ID: {self._id[:8]}...\n"
            f"  Адрес: {self._address}\n"
            f"  Площадь: {self._area:.1f} м²\n"
            f"  Комнат: {self._rooms}\n"
            f"  Цена: {self._price:,.0f} руб./мес\n"
            f"  Статус: {self._status}\n"
            f"  Добавлен: {self._date_added[:19]}"
        )

    def to_short_string(self) -> str:
        """
        Возвращает краткое строковое представление объекта.
        Используется для вывода в списках и таблицах.
        """
        return (
            f"{self._address} | {self._area:.1f} м² | "
            f"{self._rooms} комн. | {self._price:,.0f} руб."
        )

    # ── Реализация интерфейса Comparable ──────────────────────────────────
    def compare_to(self, other: Any) -> int:
        """
        Сравнивает объекты по цене.

        Args:
            other: объект для сравнения.

        Returns:
            int: -1 если текущий дешевле, 0 если цены равны,
                 1 если текущий дороже.

        Raises:
            TypeError: если other не является экземпляром Apartment.
        """
        if not isinstance(other, Apartment):
            raise TypeError(
                "Можно сравнивать только с объектами типа Apartment"
            )
        if self._price < other._price:
            return -1
        elif self._price > other._price:
            return 1
        else:
            return 0

    # ── Магические методы ─────────────────────────────────────────────────
    def __str__(self) -> str:
        """Возвращает читаемое строковое представление (вызов print())."""
        return self.to_short_string()

    def __repr__(self) -> str:
        """Возвращает техническое строковое представление (отладка)."""
        return (
            f"Apartment(id={self._id!r}, address={self._address!r}, "
            f"area={self._area}, price={self._price}, rooms={self._rooms})"
        )

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает объекты по идентификатору.

        Два объекта считаются равными, если у них совпадает ID.
        """
        if not isinstance(other, Apartment):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        """Возвращает хеш объекта по идентификатору."""
        return hash(self._id)

    # ── Метод класса ──────────────────────────────────────────────────────
    @classmethod
    def get_total_count(cls) -> int:
        """
        Возвращает общее количество созданных объектов Apartment.

        Returns:
            int: количество экземпляров за всё время работы.
        """
        return cls._total_count

    # ── Сериализация ──────────────────────────────────────────────────────
    def to_dict(self) -> dict[str, Any]:
        """
        Сериализует объект в словарь для сохранения в JSON.

        Returns:
            dict[str, Any]: словарь со всеми атрибутами объекта.
        """
        return {
            "type": self.__class__.__name__,
            "id": self._id,
            "address": self._address,
            "area": self._area,
            "price": self._price,
            "rooms": self._rooms,
            "date_added": self._date_added,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Apartment":
        """
        Восстанавливает объект из словаря (без вызова __init__).

        Args:
            data: словарь с сохранёнными данными объекта.

        Returns:
            Apartment: восстановленный объект.
        """
        instance = cls.__new__(cls)
        instance._id = data["id"]
        instance._address = data["address"]
        instance._area = float(data["area"])
        instance._price = float(data["price"])
        instance._rooms = int(data["rooms"])
        instance._date_added = data["date_added"]
        instance._status = data["status"]
        return instance


# ══════════════════════════════════════════════════════════════════════════
# ПРОИЗВОДНЫЙ КЛАСС: ЖИЛАЯ КВАРТИРА
# ══════════════════════════════════════════════════════════════════════════

class ResidentialApartment(Apartment):
    """
    Жилая квартира — производный класс от Apartment.

    Дополнительные атрибуты:
        _has_balcony (bool): наличие балкона.
        _floor (int): этаж расположения квартиры.

    Переопределяет методы интерфейсов Printable и Comparable.
    """

    def __init__(
        self,
        address: str,
        area: float,
        price: float,
        rooms: int,
        has_balcony: bool,
        floor: int,
        status: str = "available",
    ) -> None:
        """
        Инициализация жилой квартиры.

        Args:
            address: адрес квартиры.
            area: площадь в м².
            price: цена аренды в месяц (руб.).
            rooms: количество комнат.
            has_balcony: наличие балкона.
            floor: этаж (от 1 до 200).
            status: статус объекта.

        Raises:
            TypeError: если тип аргумента не соответствует ожидаемому.
            ValueError: если значение аргумента вне допустимого диапазона.
        """
        super().__init__(address, area, price, rooms, status)
        self._has_balcony: bool = self._validate_has_balcony(has_balcony)
        self._floor: int = self._validate_floor(floor)

    # ── Валидация ─────────────────────────────────────────────────────────
    @staticmethod
    def _validate_has_balcony(has_balcony: bool) -> bool:
        """Проверяет корректность признака балкона."""
        if not isinstance(has_balcony, bool):
            raise TypeError(
                f"Признак балкона должен быть bool, "
                f"получен {type(has_balcony).__name__}"
            )
        return has_balcony

    @staticmethod
    def _validate_floor(floor: int) -> int:
        """Проверяет корректность этажа."""
        if not isinstance(floor, int):
            raise TypeError(
                f"Этаж должен быть целым числом, "
                f"получен {type(floor).__name__}"
            )
        if floor < 1:
            raise ValueError(
                f"Этаж не может быть меньше 1, получено: {floor}"
            )
        if floor > 200:
            raise ValueError(
                f"Этаж не может быть больше 200, получено: {floor}"
            )
        return floor

    # ── Свойства ──────────────────────────────────────────────────────────
    @property
    def has_balcony(self) -> bool:
        """Наличие балкона (только чтение)."""
        return self._has_balcony

    @property
    def floor(self) -> int:
        """Этаж (только чтение)."""
        return self._floor

    # ── Бизнес-методы ─────────────────────────────────────────────────────
    def is_suitable_for_family(self, min_rooms: int = 2) -> bool:
        """
        Проверяет, подходит ли квартира для семьи.

        Квартира считается подходящей, если количество комнат
        не меньше заданного и площадь не менее 40 м².

        Args:
            min_rooms: минимальное количество комнат (по умолчанию 2).

        Returns:
            bool: True если квартира подходит для семьи.
        """
        return self._rooms >= min_rooms and self._area >= 40

    # ── Переопределение интерфейса Printable ──────────────────────────────
    def to_string(self) -> str:
        """Полное строковое представление жилой квартиры."""
        balcony: str = "есть" if self._has_balcony else "нет"
        return (
            f"Жилая квартира\n"
            f"  ID: {self._id[:8]}...\n"
            f"  Адрес: {self._address}\n"
            f"  Площадь: {self._area:.1f} м²\n"
            f"  Комнат: {self._rooms}\n"
            f"  Этаж: {self._floor}\n"
            f"  Балкон: {balcony}\n"
            f"  Цена: {self._price:,.0f} руб./мес\n"
            f"  Статус: {self._status}\n"
            f"  Добавлен: {self._date_added[:19]}"
        )

    def to_short_string(self) -> str:
        """Краткое строковое представление жилой квартиры."""
        balcony: str = "балкон" if self._has_balcony else "без балкона"
        return (
            f"Жилая: {self._address} | {self._area:.1f} м² | "
            f"этаж {self._floor} | {balcony} | {self._price:,.0f} руб."
        )

    # ── Переопределение интерфейса Comparable ─────────────────────────────
    def compare_to(self, other: Any) -> int:
        """
        Сравнивает жилые квартиры по цене за квадратный метр.

        Args:
            other: объект для сравнения.

        Returns:
            int: результат сравнения (-1, 0, 1).

        Raises:
            TypeError: если other не является экземпляром Apartment.
        """
        if not isinstance(other, Apartment):
            raise TypeError(
                "Можно сравнивать только с объектами типа Apartment"
            )
        self_ppsm: float = self.price_per_sqm()
        other_ppsm: float = other.price_per_sqm()

        if self_ppsm < other_ppsm:
            return -1
        elif self_ppsm > other_ppsm:
            return 1
        else:
            return 0

    # ── Сериализация ──────────────────────────────────────────────────────
    def to_dict(self) -> dict[str, Any]:
        """Сериализует жилую квартиру в словарь."""
        data: dict[str, Any] = super().to_dict()
        data["has_balcony"] = self._has_balcony
        data["floor"] = self._floor
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ResidentialApartment":
        """Восстанавливает жилую квартиру из словаря."""
        instance = cls.__new__(cls)
        instance._id = data["id"]
        instance._address = data["address"]
        instance._area = float(data["area"])
        instance._price = float(data["price"])
        instance._rooms = int(data["rooms"])
        instance._date_added = data["date_added"]
        instance._status = data["status"]
        instance._has_balcony = bool(data["has_balcony"])
        instance._floor = int(data["floor"])
        return instance


# ══════════════════════════════════════════════════════════════════════════
# ПРОИЗВОДНЫЙ КЛАСС: КОММЕРЧЕСКОЕ ПОМЕЩЕНИЕ
# ══════════════════════════════════════════════════════════════════════════

class CommercialApartment(Apartment):
    """
    Коммерческое помещение — производный класс от Apartment.

    Дополнительные атрибуты:
        _business_type (str): тип бизнеса (офис, магазин, склад и т.д.).
        _has_parking (bool): наличие парковки.

    Переопределяет методы интерфейсов Printable и Comparable.
    """

    VALID_BUSINESS_TYPES: tuple[str, ...] = (
        "офис", "магазин", "склад", "ресторан", "салон", "аптека"
    )

    def __init__(
        self,
        address: str,
        area: float,
        price: float,
        rooms: int,
        business_type: str,
        has_parking: bool,
        status: str = "available",
    ) -> None:
        """
        Инициализация коммерческого помещения.

        Args:
            address: адрес помещения.
            area: площадь в м².
            price: цена аренды в месяц (руб.).
            rooms: количество помещений/комнат.
            business_type: тип бизнеса (из списка VALID_BUSINESS_TYPES).
            has_parking: наличие парковки.
            status: статус объекта.

        Raises:
            TypeError: если тип аргумента не соответствует ожидаемому.
            ValueError: если значение аргумента вне допустимого диапазона.
        """
        super().__init__(address, area, price, rooms, status)
        self._business_type: str = self._validate_business_type(business_type)
        self._has_parking: bool = self._validate_has_parking(has_parking)

    # ── Валидация ─────────────────────────────────────────────────────────
    @staticmethod
    def _validate_business_type(business_type: str) -> str:
        """Проверяет корректность типа бизнеса."""
        if not isinstance(business_type, str):
            raise TypeError(
                f"Тип бизнеса должен быть строкой, "
                f"получен {type(business_type).__name__}"
            )
        business_type = business_type.strip().lower()
        if business_type not in CommercialApartment.VALID_BUSINESS_TYPES:
            raise ValueError(
                f"Недопустимый тип бизнеса '{business_type}'. "
                f"Допустимые: {', '.join(CommercialApartment.VALID_BUSINESS_TYPES)}"
            )
        return business_type

    @staticmethod
    def _validate_has_parking(has_parking: bool) -> bool:
        """Проверяет корректность признака парковки."""
        if not isinstance(has_parking, bool):
            raise TypeError(
                f"Признак парковки должен быть bool, "
                f"получен {type(has_parking).__name__}"
            )
        return has_parking

    # ── Свойства ──────────────────────────────────────────────────────────
    @property
    def business_type(self) -> str:
        """Тип бизнеса (только чтение)."""
        return self._business_type

    @property
    def has_parking(self) -> bool:
        """Наличие парковки (только чтение)."""
        return self._has_parking

    # ── Бизнес-методы ─────────────────────────────────────────────────────
    def calculate_business_cost(self, clients_per_day: int) -> float:
        """
        Рассчитывает стоимость аренды на одного клиента в день.

        Args:
            clients_per_day: ожидаемое количество клиентов в день.

        Returns:
            float: стоимость на одного клиента в день (руб.).
        """
        daily_cost: float = self._price / 30
        return daily_cost / clients_per_day

    # ── Переопределение интерфейса Printable ──────────────────────────────
    def to_string(self) -> str:
        """Полное строковое представление коммерческого помещения."""
        parking: str = "есть" if self._has_parking else "нет"
        return (
            f"Коммерческое помещение\n"
            f"  ID: {self._id[:8]}...\n"
            f"  Адрес: {self._address}\n"
            f"  Тип: {self._business_type}\n"
            f"  Площадь: {self._area:.1f} м²\n"
            f"  Помещений: {self._rooms}\n"
            f"  Парковка: {parking}\n"
            f"  Цена: {self._price:,.0f} руб./мес\n"
            f"  Статус: {self._status}\n"
            f"  Добавлен: {self._date_added[:19]}"
        )

    def to_short_string(self) -> str:
        """Краткое строковое представление коммерческого помещения."""
        parking: str = "парковка" if self._has_parking else "без парковки"
        return (
            f"Коммерческое ({self._business_type}): {self._address} | "
            f"{self._area:.1f} м² | {parking} | {self._price:,.0f} руб."
        )

    # ── Переопределение интерфейса Comparable ─────────────────────────────
    def compare_to(self, other: Any) -> int:
        """
        Сравнивает коммерческие помещения по площади.

        Args:
            other: объект для сравнения.

        Returns:
            int: результат сравнения (-1, 0, 1).

        Raises:
            TypeError: если other не является экземпляром Apartment.
        """
        if not isinstance(other, Apartment):
            raise TypeError(
                "Можно сравнивать только с объектами типа Apartment"
            )
        if self._area < other._area:
            return -1
        elif self._area > other._area:
            return 1
        else:
            return 0

    # ── Сериализация ──────────────────────────────────────────────────────
    def to_dict(self) -> dict[str, Any]:
        """Сериализует коммерческое помещение в словарь."""
        data: dict[str, Any] = super().to_dict()
        data["business_type"] = self._business_type
        data["has_parking"] = self._has_parking
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CommercialApartment":
        """Восстанавливает коммерческое помещение из словаря."""
        instance = cls.__new__(cls)
        instance._id = data["id"]
        instance._address = data["address"]
        instance._area = float(data["area"])
        instance._price = float(data["price"])
        instance._rooms = int(data["rooms"])
        instance._date_added = data["date_added"]
        instance._status = data["status"]
        instance._business_type = str(data["business_type"])
        instance._has_parking = bool(data["has_parking"])
        return instance


# ══════════════════════════════════════════════════════════════════════════
# ФАБРИКА ДЛЯ ВОССТАНОВЛЕНИЯ ОБЪЕКТОВ ИЗ СЛОВАРЯ
# ══════════════════════════════════════════════════════════════════════════

_TYPE_MAP: dict[str, type] = {
    "Apartment": Apartment,
    "ResidentialApartment": ResidentialApartment,
    "CommercialApartment": CommercialApartment,
}


def apartment_from_dict(data: dict[str, Any]) -> Apartment:
    """
    Восстанавливает объект недвижимости из словаря.
    Автоматически определяет тип объекта по полю 'type'.

    Args:
        data: словарь с данными объекта (должен содержать ключ 'type').

    Returns:
        Apartment: восстановленный объект соответствующего класса.

    Raises:
        ValueError: если тип объекта неизвестен или отсутствует в данных.
    """
    obj_type: str = data.get("type", "")
    if not obj_type:
        raise ValueError(
            "Отсутствует поле 'type' в данных объекта"
        )
    cls: type | None = _TYPE_MAP.get(obj_type)
    if cls is None:
        raise ValueError(
            f"Неизвестный тип объекта: '{obj_type}'. "
            f"Допустимые: {', '.join(_TYPE_MAP.keys())}"
        )
    return cls.from_dict(data)

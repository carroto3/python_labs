"""
Модуль модели данных для квартиры (Apartment).
Предметная область: Недвижимость.

Реализует класс с инкапсуляцией, валидацией,
свойствами, магическими методами и бизнес-логикой.
"""


class Apartment:
    """
    Класс, представляющий квартиру в системе недвижимости.

    Атрибуты класса:
        AVAILABLE_STATUSES (tuple): допустимые статусы квартиры.
        _total_count (int): общее количество созданных объектов.

    Атрибуты экземпляра:
        _address  (str)   — адрес квартиры
        _area     (float) — площадь в м²
        _price    (float) — цена аренды в месяц (руб.)
        _rooms    (int)   — количество комнат
    """

    # ── Атрибуты класса ───────────────────────────────────────────────────
    AVAILABLE_STATUSES: tuple = ("available", "rented", "reserved")
    _total_count: int = 0

    # ── Конструктор ───────────────────────────────────────────────────────
    def __init__(
        self,
        address: str,
        area: float,
        price: float,
        rooms: int,
    ) -> None:
        """
        Инициализация квартиры с проверкой входных данных.

        Args:
            address (str)  : адрес квартиры (непустая строка, мин. 5 символов).
            area    (float): общая площадь в м² (от 1 до 10 000).
            price   (float): ежемесячная цена аренды в руб. (от 0 до 1 000 000).
            rooms   (int)  : количество комнат (от 1 до 20).

        Raises:
            TypeError : если тип аргумента не соответствует ожидаемому.
            ValueError: если значение аргумента вне допустимого диапазона.
        """
        self._address: str   = self._validate_address(address)
        self._area:    float = self._validate_area(area)
        self._price:   float = self._validate_price(price)
        self._rooms:   int   = self._validate_rooms(rooms)

        Apartment._total_count += 1

    # ── Валидация (внутренние статические методы) ─────────────────────────
    @staticmethod
    def _validate_address(address: str) -> str:
        """
        Проверяет корректность адреса.

        Raises:
            TypeError : если address не строка.
            ValueError: если адрес пустой или короче 5 символов.
        """
        if not isinstance(address, str):
            raise TypeError(
                f"Адрес должен быть строкой, "
                f"получен {type(address).__name__}"
            )
        address = address.strip()
        if len(address) == 0:
            raise ValueError(
                "Адрес не может быть пустой строкой"
            )
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
            TypeError : если area не число.
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
            TypeError : если price не число.
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
            TypeError : если rooms не целое число.
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

    # ── Свойства (только чтение) ──────────────────────────────────────────
    @property
    def address(self) -> str:
        """Адрес квартиры (только чтение)."""
        return self._address

    @property
    def area(self) -> float:
        """Площадь квартиры в м² (только чтение)."""
        return self._area

    @property
    def rooms(self) -> int:
        """Количество комнат (только чтение)."""
        return self._rooms

    # ── Свойство с сеттером ───────────────────────────────────────────────
    @property
    def price(self) -> float:
        """Цена аренды в месяц, руб."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """
        Устанавливает новую цену аренды с валидацией.

        Args:
            new_price (float): новая цена аренды в руб.

        Raises:
            TypeError : если тип не число.
            ValueError: если цена вне допустимого диапазона.
        """
        self._price = self._validate_price(new_price)

    # ── Магические методы ─────────────────────────────────────────────────
    def __str__(self) -> str:
        """
        Возвращает читаемое строковое представление квартиры.
        Используется при вызове print().
        """
        return (
            f"┌─ Квартира ───────────────────────────────┐\n"
            f"│  Адрес    : {self._address}\n"
            f"│  Площадь  : {self._area:.1f} м²\n"
            f"│  Комнат   : {self._rooms}\n"
            f"│  Цена/мес : {self._price:>12,.0f} руб.\n"
            f"└──────────────────────────────────────────┘"
        )

    def __repr__(self) -> str:
        """
        Возвращает техническое представление объекта.
        Используется при отладке и в интерактивной консоли.
        """
        return (
            f"Apartment("
            f"address={self._address!r}, "
            f"area={self._area:.1f}, "
            f"price={self._price:.2f}, "
            f"rooms={self._rooms}"
            f")"
        )

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает две квартиры по адресу и площади.

        Две квартиры считаются одинаковыми, если совпадают
        адрес (без учёта регистра) и площадь.
        """
        if not isinstance(other, Apartment):
            return NotImplemented
        return (
            self._address.lower() == other._address.lower()
            and self._area == other._area
        )

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
        Рассчитывает ежемесячные расходы арендатора с учётом налога.

        Args:
            tax_rate (float): ставка налога в диапазоне [0.0, 1.0],
                              по умолчанию 13%.

        Returns:
            float: цена аренды с учётом налога.

        Raises:
            TypeError : если tax_rate не число.
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

    # ── Метод класса ──────────────────────────────────────────────────────
    @classmethod
    def get_total_count(cls) -> int:
        """
        Возвращает общее количество созданных объектов Apartment.

        Returns:
            int: количество экземпляров.
        """
        return cls._total_count
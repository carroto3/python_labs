"""
Классы квартир с реализацией интерфейсов.
Предметная область: Недвижимость.
"""

from interfaces import Printable, Comparable


class Apartment(Printable, Comparable):
    """
    Базовый класс квартиры.
    Реализует интерфейсы Printable и Comparable.
    """

    def __init__(self, address, area, price, rooms):
        self.address = address
        self.area = area
        self.price = price
        self.rooms = rooms

    def price_per_sqm(self):
        """Цена за квадратный метр."""
        return self.price / self.area

    # Реализация интерфейса Printable
    def to_string(self):
        """Полное строковое представление."""
        return (
            f"Квартира\n"
            f"  Адрес: {self.address}\n"
            f"  Площадь: {self.area} м²\n"
            f"  Комнат: {self.rooms}\n"
            f"  Цена: {self.price} руб./мес"
        )

    def to_short_string(self):
        """Краткое строковое представление."""
        return f"{self.address} ({self.area} м², {self.price} руб.)"

    # Реализация интерфейса Comparable
    def compare_to(self, other):
        """Сравнение по цене."""
        if not isinstance(other, Apartment):
            raise TypeError("Можно сравнивать только с объектами типа Apartment")

        if self.price < other.price:
            return -1
        elif self.price > other.price:
            return 1
        else:
            return 0

    def __str__(self):
        return self.to_short_string()


class ResidentialApartment(Apartment):
    """
    Жилая квартира.
    Переопределяет методы интерфейсов для специфичного поведения.
    """

    def __init__(self, address, area, price, rooms, has_balcony, floor):
        super().__init__(address, area, price, rooms)
        self.has_balcony = has_balcony
        self.floor = floor

    def is_suitable_for_family(self, min_rooms):
        """Проверяет подходит ли для семьи."""
        return self.rooms >= min_rooms and self.area >= 40

    # Переопределение интерфейса Printable
    def to_string(self):
        """Полное строковое представление жилой квартиры."""
        balcony = "есть" if self.has_balcony else "нет"
        return (
            f"Жилая квартира\n"
            f"  Адрес: {self.address}\n"
            f"  Площадь: {self.area} м²\n"
            f"  Комнат: {self.rooms}\n"
            f"  Этаж: {self.floor}\n"
            f"  Балкон: {balcony}\n"
            f"  Цена: {self.price} руб./мес"
        )

    def to_short_string(self):
        """Краткое строковое представление жилой квартиры."""
        return f"Жилая: {self.address}, этаж {self.floor} ({self.price} руб.)"

    # Переопределение интерфейса Comparable
    def compare_to(self, other):
        """Сравнение по соотношению цена/площадь (для жилых важнее)."""
        if not isinstance(other, Apartment):
            raise TypeError("Можно сравнивать только с объектами типа Apartment")

        # Для жилых квартир сравниваем по цене за м²
        self_price_per_sqm = self.price_per_sqm()
        other_price_per_sqm = other.price_per_sqm()

        if self_price_per_sqm < other_price_per_sqm:
            return -1
        elif self_price_per_sqm > other_price_per_sqm:
            return 1
        else:
            return 0


class CommercialApartment(Apartment):
    """
    Коммерческое помещение.
    Переопределяет методы интерфейсов для специфичного поведения.
    """

    def __init__(self, address, area, price, rooms, business_type, has_parking):
        super().__init__(address, area, price, rooms)
        self.business_type = business_type
        self.has_parking = has_parking

    def calculate_business_cost(self, clients_per_day):
        """Стоимость на одного клиента в день."""
        daily_cost = self.price / 30
        return daily_cost / clients_per_day

    # Переопределение интерфейса Printable
    def to_string(self):
        """Полное строковое представление коммерческого помещения."""
        parking = "есть" if self.has_parking else "нет"
        return (
            f"Коммерческое помещение\n"
            f"  Адрес: {self.address}\n"
            f"  Тип: {self.business_type}\n"
            f"  Площадь: {self.area} м²\n"
            f"  Помещений: {self.rooms}\n"
            f"  Парковка: {parking}\n"
            f"  Цена: {self.price} руб./мес"
        )

    def to_short_string(self):
        """Краткое строковое представление коммерческого помещения."""
        return f"Коммерческое ({self.business_type}): {self.address} ({self.price} руб.)"

    # Переопределение интерфейса Comparable
    def compare_to(self, other):
        """Сравнение по площади (для коммерческих важнее размер)."""
        if not isinstance(other, Apartment):
            raise TypeError("Можно сравнивать только с объектами типа Apartment")

        # Для коммерческих помещений сравниваем по площади
        if self.area < other.area:
            return -1
        elif self.area > other.area:
            return 1
        else:
            return 0
"""
Демонстрация работы с интерфейсами.
Предметная область: Недвижимость.
"""

from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════════════════════
# ИНТЕРФЕЙСЫ (из interfaces.py)
# ══════════════════════════════════════════════════════════════════════════

class Printable(ABC):
    """Интерфейс для объектов, которые можно выводить в разных форматах."""

    @abstractmethod
    def to_string(self):
        """Возвращает полное строковое представление объекта."""
        pass

    @abstractmethod
    def to_short_string(self):
        """Возвращает краткое строковое представление объекта."""
        pass


class Comparable(ABC):
    """Интерфейс для объектов, которые можно сравнивать."""

    @abstractmethod
    def compare_to(self, other):
        """Сравнивает текущий объект с другим."""
        pass


# ══════════════════════════════════════════════════════════════════════════
# КЛАССЫ (из models.py)
# ══════════════════════════════════════════════════════════════════════════

class Apartment(Printable, Comparable):
    """Базовый класс квартиры."""

    def __init__(self, address, area, price, rooms):
        self.address = address
        self.area = area
        self.price = price
        self.rooms = rooms

    def price_per_sqm(self):
        return self.price / self.area

    def to_string(self):
        return (
            f"Квартира\n"
            f"  Адрес: {self.address}\n"
            f"  Площадь: {self.area} м²\n"
            f"  Комнат: {self.rooms}\n"
            f"  Цена: {self.price} руб./мес"
        )

    def to_short_string(self):
        return f"{self.address} ({self.area} м², {self.price} руб.)"

    def compare_to(self, other):
        if not isinstance(other, Apartment):
            raise TypeError("Можно сравнивать только с объектами типа Apartment")
        if self.price < other.price:
            return -1
        elif self.price > other.price:
            return 1
        else:
            return 0


class ResidentialApartment(Apartment):
    """Жилая квартира."""

    def __init__(self, address, area, price, rooms, has_balcony, floor):
        super().__init__(address, area, price, rooms)
        self.has_balcony = has_balcony
        self.floor = floor

    def is_suitable_for_family(self, min_rooms):
        return self.rooms >= min_rooms and self.area >= 40

    def to_string(self):
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
        return f"Жилая: {self.address}, этаж {self.floor} ({self.price} руб.)"

    def compare_to(self, other):
        if not isinstance(other, Apartment):
            raise TypeError("Можно сравнивать только с объектами типа Apartment")
        self_price_per_sqm = self.price_per_sqm()
        other_price_per_sqm = other.price_per_sqm()
        if self_price_per_sqm < other_price_per_sqm:
            return -1
        elif self_price_per_sqm > other_price_per_sqm:
            return 1
        else:
            return 0


class CommercialApartment(Apartment):
    """Коммерческое помещение."""

    def __init__(self, address, area, price, rooms, business_type, has_parking):
        super().__init__(address, area, price, rooms)
        self.business_type = business_type
        self.has_parking = has_parking

    def calculate_business_cost(self, clients_per_day):
        daily_cost = self.price / 30
        return daily_cost / clients_per_day

    def to_string(self):
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
        return f"Коммерческое ({self.business_type}): {self.address} ({self.price} руб.)"

    def compare_to(self, other):
        if not isinstance(other, Apartment):
            raise TypeError("Можно сравнивать только с объектами типа Apartment")
        if self.area < other.area:
            return -1
        elif self.area > other.area:
            return 1
        else:
            return 0


# ══════════════════════════════════════════════════════════════════════════
# ДЕМОНСТРАЦИЯ
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ИНТЕРФЕЙСОВ (ABC)")
    print("=" * 70)

    # Создание объектов
    print("\n1. Создание объектов")
    print("-" * 70)

    apt1 = Apartment(
        address="ул. Ленина, д. 10, кв. 5",
        area=54.5,
        price=35000,
        rooms=2
    )

    apt2 = ResidentialApartment(
        address="пр. Мира, д. 3, кв. 12",
        area=80.0,
        price=55000,
        rooms=3,
        has_balcony=True,
        floor=5
    )

    apt3 = CommercialApartment(
        address="Невский пр., д. 100, пом. 1",
        area=120.0,
        price=150000,
        rooms=4,
        business_type="офис",
        has_parking=True
    )

    print("Создано 3 объекта разных типов")

    # Демонстрация интерфейса Printable
    print("\n" + "=" * 70)
    print("2. Интерфейс Printable - метод to_string()")
    print("-" * 70)

    print("\nБазовый класс Apartment:")
    print(apt1.to_string())

    print("\nПроизводный класс ResidentialApartment:")
    print(apt2.to_string())

    print("\nПроизводный класс CommercialApartment:")
    print(apt3.to_string())

    # Демонстрация to_short_string()
    print("\n" + "=" * 70)
    print("3. Интерфейс Printable - метод to_short_string()")
    print("-" * 70)

    apartments = [apt1, apt2, apt3]

    for i, apt in enumerate(apartments, 1):
        print(f"{i}. {apt.to_short_string()}")

    # Демонстрация интерфейса Comparable
    print("\n" + "=" * 70)
    print("4. Интерфейс Comparable - метод compare_to()")
    print("-" * 70)

    print("\nСравнение Apartment (по цене):")
    result = apt1.compare_to(apt2)
    if result < 0:
        print(f"  '{apt1.to_short_string()}' дешевле")
    elif result > 0:
        print(f"  '{apt1.to_short_string()}' дороже")
    else:
        print(f"  Цены равны")

    print("\nСравнение ResidentialApartment (по цене за м²):")
    apt4 = ResidentialApartment(
        address="ул. Пушкина, д. 7",
        area=50.0,
        price=40000,
        rooms=2,
        has_balcony=False,
        floor=3
    )
    result = apt2.compare_to(apt4)
    print(f"  {apt2.to_short_string()}: {apt2.price_per_sqm():.2f} руб./м²")
    print(f"  {apt4.to_short_string()}: {apt4.price_per_sqm():.2f} руб./м²")
    if result < 0:
        print(f"  Первая дешевле за м²")
    elif result > 0:
        print(f"  Первая дороже за м²")
    else:
        print(f"  Цены за м² равны")

    print("\nСравнение CommercialApartment (по площади):")
    apt5 = CommercialApartment(
        address="ул. Гороховая, д. 5",
        area=80.0,
        price=100000,
        rooms=3,
        business_type="магазин",
        has_parking=False
    )
    result = apt3.compare_to(apt5)
    print(f"  {apt3.to_short_string()}: {apt3.area} м²")
    print(f"  {apt5.to_short_string()}: {apt5.area} м²")
    if result < 0:
        print(f"  Первое помещение меньше")
    elif result > 0:
        print(f"  Первое помещение больше")
    else:
        print(f"  Площади равны")

    # Полиморфизм через интерфейсы
    print("\n" + "=" * 70)
    print("5. Полиморфизм через единый интерфейс")
    print("-" * 70)

    all_apartments = [apt1, apt2, apt3, apt4, apt5]

    print("\nВсе объекты через метод to_short_string():")
    for i, apt in enumerate(all_apartments, 1):
        print(f"{i}. {apt.to_short_string()}")

    print("\nСортировка через метод compare_to():")
    sorted_apts = all_apartments.copy()
    n = len(sorted_apts)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_apts[j].compare_to(sorted_apts[j + 1]) > 0:
                sorted_apts[j], sorted_apts[j + 1] = sorted_apts[j + 1], sorted_apts[j]

    print("\nОтсортированный список (критерий зависит от типа):")
    for i, apt in enumerate(sorted_apts, 1):
        print(f"{i}. {type(apt).__name__}: {apt.to_short_string()}")

    # Проверка isinstance
    print("\n" + "=" * 70)
    print("6. Проверка реализации интерфейсов")
    print("-" * 70)

    print(f"\napt1 (Apartment) является Printable? {isinstance(apt1, Printable)}")
    print(f"apt1 (Apartment) является Comparable? {isinstance(apt1, Comparable)}")

    print(f"\napt2 (ResidentialApartment) является Printable? {isinstance(apt2, Printable)}")
    print(f"apt2 (ResidentialApartment) является Comparable? {isinstance(apt2, Comparable)}")

    print(f"\napt3 (CommercialApartment) является Printable? {isinstance(apt3, Printable)}")
    print(f"apt3 (CommercialApartment) является Comparable? {isinstance(apt3, Comparable)}")

    # Итог
    print("\n" + "=" * 70)
    print("ИТОГ")
    print("=" * 70)

    print("\nРеализовано интерфейсов: 2")
    print("  1. Printable (to_string, to_short_string)")
    print("  2. Comparable (compare_to)")

    print("\nКлассов, реализующих интерфейсы: 3")
    print("  1. Apartment")
    print("  2. ResidentialApartment")
    print("  3. CommercialApartment")

    print("\nОсобенности реализации:")
    print("  - Apartment: сравнение по цене")
    print("  - ResidentialApartment: сравнение по цене за м²")
    print("  - CommercialApartment: сравнение по площади")

    print("\nДемонстрация завершена.")
"""
Демонстрация функций-стратегий и фильтров.
Предметная область: Недвижимость.
"""


# ══════════════════════════════════════════════════════════════════════════
# КЛАССЫ КВАРТИР
# ══════════════════════════════════════════════════════════════════════════

class Apartment:
    """Базовый класс квартиры."""

    def __init__(self, address, area, price, rooms):
        self.address = address
        self.area = area
        self.price = price
        self.rooms = rooms

    def price_per_sqm(self):
        return self.price / self.area

    def __str__(self):
        return f"{self.address} | {self.area} м² | {self.rooms} комн. | {self.price:,} руб."


class ResidentialApartment(Apartment):
    """Жилая квартира."""

    def __init__(self, address, area, price, rooms, has_balcony, floor):
        super().__init__(address, area, price, rooms)
        self.has_balcony = has_balcony
        self.floor = floor

    def __str__(self):
        balcony = "балкон" if self.has_balcony else "без балкона"
        return f"Жилая: {self.address} | {self.area} м² | этаж {self.floor} | {balcony} | {self.price:,} руб."


class CommercialApartment(Apartment):
    """Коммерческое помещение."""

    def __init__(self, address, area, price, rooms, business_type, has_parking):
        super().__init__(address, area, price, rooms)
        self.business_type = business_type
        self.has_parking = has_parking

    def __str__(self):
        parking = "парковка" if self.has_parking else "без парковки"
        return f"Коммерческое ({self.business_type}): {self.address} | {self.area} м² | {parking} | {self.price:,} руб."


# ══════════════════════════════════════════════════════════════════════════
# КОЛЛЕКЦИЯ
# ══════════════════════════════════════════════════════════════════════════

class ApartmentCollection:
    """Коллекция квартир с поддержкой стратегий."""

    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def get_all(self):
        return self._items

    def sort_by(self, strategy):
        """Сортировка через функцию-стратегию."""
        return sorted(self._items, key=strategy)

    def filter_by(self, filter_func):
        """Фильтрация через функцию-фильтр."""
        return list(filter(filter_func, self._items))

    def __len__(self):
        return len(self._items)


# ══════════════════════════════════════════════════════════════════════════
# СТРАТЕГИИ СОРТИРОВКИ
# ══════════════════════════════════════════════════════════════════════════

def by_price(apartment):
    """Сортировка по цене."""
    return apartment.price


def by_area(apartment):
    """Сортировка по площади."""
    return apartment.area


def by_price_per_sqm(apartment):
    """Сортировка по цене за м²."""
    return apartment.price / apartment.area


# ══════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ-ФИЛЬТРЫ
# ══════════════════════════════════════════════════════════════════════════

def is_affordable(apartment):
    """Фильтр: доступные квартиры (до 50000 руб.)."""
    return apartment.price <= 50000


def is_spacious(apartment):
    """Фильтр: просторные квартиры (от 60 м²)."""
    return apartment.area >= 60


def is_residential(apartment):
    """Фильтр: только жилые квартиры."""
    return hasattr(apartment, 'floor')


def is_commercial(apartment):
    """Фильтр: только коммерческие помещения."""
    return hasattr(apartment, 'business_type')


# ══════════════════════════════════════════════════════════════════════════
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
# ══════════════════════════════════════════════════════════════════════════

def print_list(apartments, title):
    """Выводит список квартир с заголовком."""
    print(f"\n{title}")
    print("-" * 80)
    for i, apt in enumerate(apartments, 1):
        ppsm = apt.price_per_sqm()
        print(f"{i}. {apt}")
        print(f"   Цена за м²: {ppsm:,.2f} руб.")


# ══════════════════════════════════════════════════════════════════════════
# ДЕМОНСТРАЦИЯ
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("ДЕМОНСТРАЦИЯ ФУНКЦИЙ-СТРАТЕГИЙ И ФИЛЬТРОВ")
    print("=" * 80)

    # Создание коллекции
    print("\n1. Создание коллекции квартир")
    print("-" * 80)

    collection = ApartmentCollection()

    # Добавление объектов (минимум 5)
    collection.add(Apartment(
        address="ул. Ленина, д. 10, кв. 5",
        area=54.5,
        price=35000,
        rooms=2
    ))

    collection.add(ResidentialApartment(
        address="пр. Мира, д. 3, кв. 12",
        area=80.0,
        price=55000,
        rooms=3,
        has_balcony=True,
        floor=5
    ))

    collection.add(CommercialApartment(
        address="Невский пр., д. 100, пом. 1",
        area=120.0,
        price=150000,
        rooms=4,
        business_type="офис",
        has_parking=True
    ))

    collection.add(ResidentialApartment(
        address="ул. Пушкина, д. 7, кв. 22",
        area=42.0,
        price=28000,
        rooms=1,
        has_balcony=False,
        floor=3
    ))

    collection.add(CommercialApartment(
        address="ул. Гороховая, д. 5, пом. 3",
        area=65.0,
        price=85000,
        rooms=3,
        business_type="магазин",
        has_parking=False
    ))

    collection.add(ResidentialApartment(
        address="наб. Фонтанки, д. 15, кв. 8",
        area=95.0,
        price=75000,
        rooms=4,
        has_balcony=True,
        floor=7
    ))

    print(f"Добавлено квартир: {len(collection)}")

    # Исходная коллекция
    print_list(collection.get_all(), "Исходная коллекция (без сортировки):")

    # ══════════════════════════════════════════════════════════════════════
    # СОРТИРОВКА (3 стратегии)
    # ══════════════════════════════════════════════════════════════════════

    print("\n" + "=" * 80)
    print("2. СОРТИРОВКА ПО РАЗНЫМ СТРАТЕГИЯМ")
    print("=" * 80)

    # Стратегия 1: По цене
    sorted_by_price = collection.sort_by(by_price)
    print_list(sorted_by_price, "Стратегия 1: Сортировка по цене (по возрастанию)")

    # Стратегия 2: По площади
    sorted_by_area = collection.sort_by(by_area)
    print_list(sorted_by_area, "Стратегия 2: Сортировка по площади (по возрастанию)")

    # Стратегия 3: По цене за м²
    sorted_by_ppsm = collection.sort_by(by_price_per_sqm)
    print_list(sorted_by_ppsm, "Стратегия 3: Сортировка по цене за м² (по возрастанию)")

    # Дополнительно: сортировка с lambda
    print("\n" + "-" * 80)
    print("Дополнительно: Сортировка по цене (по убыванию) с lambda:")
    print("-" * 80)
    sorted_by_price_desc = sorted(collection.get_all(), key=lambda x: x.price, reverse=True)
    for i, apt in enumerate(sorted_by_price_desc, 1):
        print(f"{i}. {apt}")

    # ══════════════════════════════════════════════════════════════════════
    # ФИЛЬТРАЦИЯ (2+ фильтра)
    # ══════════════════════════════════════════════════════════════════════

    print("\n" + "=" * 80)
    print("3. ФИЛЬТРАЦИЯ ПО РАЗНЫМ КРИТЕРИЯМ")
    print("=" * 80)

    # Фильтр 1: Доступные квартиры (до 50000 руб.)
    affordable = collection.filter_by(is_affordable)
    print_list(affordable, f"Фильтр 1: Доступные квартиры (до 50,000 руб.) — найдено: {len(affordable)}")

    # Фильтр 2: Просторные квартиры (от 60 м²)
    spacious = collection.filter_by(is_spacious)
    print_list(spacious, f"Фильтр 2: Просторные квартиры (от 60 м²) — найдено: {len(spacious)}")

    # Дополнительные фильтры
    print("\n" + "-" * 80)
    print("Дополнительные фильтры:")
    print("-" * 80)

    # Фильтр 3: Только жилые
    residential = collection.filter_by(is_residential)
    print(f"\nФильтр 3: Только жилые квартиры — найдено: {len(residential)}")
    for i, apt in enumerate(residential, 1):
        print(f"{i}. {apt}")

    # Фильтр 4: Только коммерческие
    commercial = collection.filter_by(is_commercial)
    print(f"\nФильтр 4: Только коммерческие помещения — найдено: {len(commercial)}")
    for i, apt in enumerate(commercial, 1):
        print(f"{i}. {apt}")

    # Фильтр с lambda
    print("\n" + "-" * 80)
    print("Фильтр с lambda: Квартиры с 2+ комнатами:")
    print("-" * 80)
    multi_room = list(filter(lambda x: x.rooms >= 2, collection.get_all()))
    for i, apt in enumerate(multi_room, 1):
        print(f"{i}. {apt} | {apt.rooms} комн.")

    # ══════════════════════════════════════════════════════════════════════
    # КОМБИНИРОВАНИЕ
    # ══════════════════════════════════════════════════════════════════════

    print("\n" + "=" * 80)
    print("4. КОМБИНИРОВАНИЕ ФИЛЬТРАЦИИ И СОРТИРОВКИ")
    print("=" * 80)

    # Сначала фильтруем, потом сортируем
    print("\nПример: Доступные квартиры, отсортированные по площади:")
    print("-" * 80)
    affordable_sorted = sorted(affordable, key=by_area)
    for i, apt in enumerate(affordable_sorted, 1):
        print(f"{i}. {apt}")

    # ══════════════════════════════════════════════════════════════════════
    # ИСПОЛЬЗОВАНИЕ MAP
    # ══════════════════════════════════════════════════════════════════════

    print("\n" + "=" * 80)
    print("5. ИСПОЛЬЗОВАНИЕ MAP")
    print("=" * 80)

    print("\nИзвлечение всех цен через map:")
    prices = list(map(lambda x: x.price, collection.get_all()))
    print(f"Цены: {prices}")
    print(f"Средняя цена: {sum(prices) / len(prices):,.2f} руб.")

    print("\nИзвлечение площадей через map:")
    areas = list(map(lambda x: x.area, collection.get_all()))
    print(f"Площади: {areas}")
    print(f"Средняя площадь: {sum(areas) / len(areas):.2f} м²")

    # ══════════════════════════════════════════════════════════════════════
    # ИТОГ
    # ══════════════════════════════════════════════════════════════════════

    print("\n" + "=" * 80)
    print("ИТОГ")
    print("=" * 80)

    print("\nРеализовано стратегий сортировки: 3")
    print("  1. by_price — по цене")
    print("  2. by_area — по площади")
    print("  3. by_price_per_sqm — по цене за м²")

    print("\nРеализовано функций-фильтров: 4")
    print("  1. is_affordable — доступные по цене")
    print("  2. is_spacious — просторные по площади")
    print("  3. is_residential — только жилые")
    print("  4. is_commercial — только коммерческие")

    print("\nИспользованные функции высшего порядка:")
    print("  - sorted(collection, key=strategy)")
    print("  - filter(filter_func, collection)")
    print("  - map(lambda, collection)")

    print("\nДемонстрация завершена.")
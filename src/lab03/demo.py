"""
Демонстрация наследования классов.
Предметная область: Недвижимость.
"""


# ══════════════════════════════════════════════════════════════════════════
# БАЗОВЫЙ КЛАСС (из base.py)
# ══════════════════════════════════════════════════════════════════════════

class Apartment:
    """Базовый класс квартиры."""

    def __init__(self, address, area, price, rooms):
        self.address = address
        self.area = area
        self.price = price
        self.rooms = rooms

    def price_per_sqm(self):
        """Цена за квадратный метр."""
        return self.price / self.area

    def __str__(self):
        return f"Квартира: {self.address}, {self.area} м², {self.rooms} комн., {self.price} руб."


# ══════════════════════════════════════════════════════════════════════════
# ПРОИЗВОДНЫЕ КЛАССЫ (из models.py)
# ══════════════════════════════════════════════════════════════════════════

class ResidentialApartment(Apartment):
    """Жилая квартира."""

    def __init__(self, address, area, price, rooms, has_balcony, floor):
        super().__init__(address, area, price, rooms)
        self.has_balcony = has_balcony
        self.floor = floor

    def is_suitable_for_family(self, min_rooms):
        """Проверяет подходит ли для семьи."""
        return self.rooms >= min_rooms and self.area >= 40

    def __str__(self):
        balcony = "есть" if self.has_balcony else "нет"
        return f"Жилая квартира: {self.address}, {self.area} м², {self.rooms} комн., этаж {self.floor}, балкон {balcony}, {self.price} руб."


class CommercialApartment(Apartment):
    """Коммерческое помещение."""

    def __init__(self, address, area, price, rooms, business_type, has_parking):
        super().__init__(address, area, price, rooms)
        self.business_type = business_type
        self.has_parking = has_parking

    def calculate_business_cost(self, clients_per_day):
        """Стоимость на одного клиента в день."""
        daily_cost = self.price / 30
        return daily_cost / clients_per_day

    def __str__(self):
        parking = "есть" if self.has_parking else "нет"
        return f"Коммерческое помещение: {self.address}, тип: {self.business_type}, {self.area} м², парковка {parking}, {self.price} руб."


# ══════════════════════════════════════════════════════════════════════════
# ДЕМОНСТРАЦИЯ
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ НАСЛЕДОВАНИЯ КЛАССОВ")
    print("=" * 60)

    # 1. Базовый класс
    print("\n1. Базовый класс Apartment")
    print("-" * 60)

    base_apt = Apartment(
        address="ул. Ленина, д. 10, кв. 5",
        area=54.5,
        price=35000,
        rooms=2
    )

    print(f"Создан: {base_apt}")
    print(f"Цена за м²: {base_apt.price_per_sqm():.2f} руб.")

    # 2. Жилая квартира
    print("\n2. Производный класс ResidentialApartment")
    print("-" * 60)

    res_apt = ResidentialApartment(
        address="пр. Мира, д. 3, кв. 12",
        area=80.0,
        price=55000,
        rooms=3,
        has_balcony=True,
        floor=5
    )

    print(f"Создан: {res_apt}")
    print(f"Метод базового класса - Цена за м²: {res_apt.price_per_sqm():.2f} руб.")
    print(f"Метод производного класса - Подходит для семьи (2+ комн.)? {res_apt.is_suitable_for_family(2)}")

    # 3. Коммерческое помещение
    print("\n3. Производный класс CommercialApartment")
    print("-" * 60)

    comm_apt = CommercialApartment(
        address="Невский пр., д. 100, пом. 1",
        area=120.0,
        price=150000,
        rooms=4,
        business_type="офис",
        has_parking=True
    )

    print(f"Создан: {comm_apt}")
    print(f"Метод базового класса - Цена за м²: {comm_apt.price_per_sqm():.2f} руб.")
    clients = 50
    cost = comm_apt.calculate_business_cost(clients)
    print(f"Метод производного класса - Стоимость на клиента (50 кл./день): {cost:.2f} руб.")

    # 4. Проверка isinstance
    print("\n4. Проверка наследования (isinstance)")
    print("-" * 60)

    print(f"res_apt является ResidentialApartment? {isinstance(res_apt, ResidentialApartment)}")
    print(f"res_apt является Apartment? {isinstance(res_apt, Apartment)}")
    print(f"comm_apt является CommercialApartment? {isinstance(comm_apt, CommercialApartment)}")
    print(f"comm_apt является Apartment? {isinstance(comm_apt, Apartment)}")

    # 5. Список объектов
    print("\n5. Работа со списком разных типов")
    print("-" * 60)

    all_apartments = [base_apt, res_apt, comm_apt]

    for i, apt in enumerate(all_apartments, 1):
        print(f"\n{i}. {type(apt).__name__}")
        print(f"   {apt}")

    # Итог
    print("\n" + "=" * 60)
    print("ИТОГ")
    print("=" * 60)

    print("\nСоздано объектов:")
    print("  - Базовый класс (Apartment): 1")
    print("  - Производный класс (ResidentialApartment): 1")
    print("  - Производный класс (CommercialApartment): 1")

    print("\nИерархия:")
    print("  Apartment")
    print("   ├── ResidentialApartment")
    print("   └── CommercialApartment")

    print("\nДемонстрация завершена.")
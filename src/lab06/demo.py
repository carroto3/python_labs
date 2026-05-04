"""
Демонстрация типизированной коллекции.
Предметная область: Недвижимость.
"""

from typing import List


# ══════════════════════════════════════════════════════════════════════════
# КЛАСС APARTMENT С ТИПАМИ (из ЛР-1)
# ══════════════════════════════════════════════════════════════════════════

class Apartment:
    """
    Класс квартиры с полными аннотациями типов.
    """

    AVAILABLE_STATUSES: tuple = ("available", "rented", "reserved")
    _total_count: int = 0

    def __init__(
        self,
        address: str,
        area: float,
        price: float,
        rooms: int,
    ) -> None:
        """
        Инициализация квартиры.
        
        Args:
            address: адрес квартиры
            area: площадь в м²
            price: цена аренды в месяц (руб.)
            rooms: количество комнат
        """
        self._address: str = address
        self._area: float = float(area)
        self._price: float = float(price)
        self._rooms: int = rooms

        Apartment._total_count += 1

    @property
    def address(self) -> str:
        """Адрес квартиры."""
        return self._address

    @property
    def area(self) -> float:
        """Площадь квартиры в м²."""
        return self._area

    @property
    def price(self) -> float:
        """Цена аренды в месяц."""
        return self._price

    @property
    def rooms(self) -> int:
        """Количество комнат."""
        return self._rooms

    def price_per_sqm(self) -> float:
        """
        Рассчитывает цену за квадратный метр.
        
        Returns:
            цена за 1 м²
        """
        return self._price / self._area

    @classmethod
    def get_total_count(cls) -> int:
        """
        Возвращает общее количество созданных объектов.
        
        Returns:
            количество экземпляров
        """
        return cls._total_count

    def __str__(self) -> str:
        """Строковое представление."""
        return (
            f"Квартира: {self._address}, "
            f"{self._area} м², "
            f"{self._rooms} комн., "
            f"{self._price:,.0f} руб."
        )

    def __repr__(self) -> str:
        """Техническое представление."""
        return (
            f"Apartment(address={self._address!r}, "
            f"area={self._area}, price={self._price}, rooms={self._rooms})"
        )


# ══════════════════════════════════════════════════════════════════════════
# ТИПИЗИРОВАННАЯ КОЛЛЕКЦИЯ
# ══════════════════════════════════════════════════════════════════════════

from typing import TypeVar, Generic, Optional

T = TypeVar('T')


class TypedCollection(Generic[T]):
    """Обобщённая коллекция."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def add(self, item: T) -> None:
        """Добавляет элемент."""
        self._items.append(item)

    def remove(self, item: T) -> None:
        """Удаляет элемент."""
        if item not in self._items:
            raise ValueError("Элемент не найден в коллекции")
        self._items.remove(item)

    def get_all(self) -> List[T]:
        """Возвращает все элементы."""
        return self._items.copy()

    def find(self, predicate) -> Optional[T]:
        """Находит элемент по условию."""
        for item in self._items:
            if predicate(item):
                return item
        return None

    def __len__(self) -> int:
        """Возвращает количество элементов."""
        return len(self._items)

    def __iter__(self):
        """Итератор."""
        return iter(self._items)


# ══════════════════════════════════════════════════════════════════════════
# ДЕМОНСТРАЦИЯ
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ТИПИЗИРОВАННОЙ КОЛЛЕКЦИИ (GENERICS)")
    print("=" * 70)

    # ──────────────────────────────────────────────────────────────────────
    # 1. Создание типизированной коллекции
    # ──────────────────────────────────────────────────────────────────────
    print("\n1. Создание типизированной коллекции Apartment")
    print("-" * 70)

    # Создаём коллекцию с явным указанием типа
    collection: TypedCollection[Apartment] = TypedCollection[Apartment]()
    print(f"Создана: {collection}")
    print(f"Тип коллекции: TypedCollection[Apartment]")
    print(f"Элементов в коллекции: {len(collection)}")

    # ──────────────────────────────────────────────────────────────────────
    # 2. Создание объектов с аннотациями типов
    # ──────────────────────────────────────────────────────────────────────
    print("\n2. Создание объектов Apartment")
    print("-" * 70)

    apt1: Apartment = Apartment(
        address="ул. Ленина, д. 10, кв. 5",
        area=54.5,
        price=35000,
        rooms=2
    )
    print(f"Создан: {apt1}")

    apt2: Apartment = Apartment(
        address="пр. Мира, д. 3, кв. 12",
        area=80.0,
        price=55000,
        rooms=3
    )
    print(f"Создан: {apt2}")

    apt3: Apartment = Apartment(
        address="ул. Пушкина, д. 7, кв. 22",
        area=42.0,
        price=28000,
        rooms=1
    )
    print(f"Создан: {apt3}")

    apt4: Apartment = Apartment(
        address="наб. Фонтанки, д. 15, кв. 8",
        area=95.0,
        price=75000,
        rooms=4
    )
    print(f"Создан: {apt4}")

    # ──────────────────────────────────────────────────────────────────────
    # 3. Добавление объектов в типизированную коллекцию
    # ──────────────────────────────────────────────────────────────────────
    print("\n3. Добавление объектов в коллекцию")
    print("-" * 70)

    collection.add(apt1)
    print(f"Добавлена: {apt1.address}")

    collection.add(apt2)
    print(f"Добавлена: {apt2.address}")

    collection.add(apt3)
    print(f"Добавлена: {apt3.address}")

    collection.add(apt4)
    print(f"Добавлена: {apt4.address}")

    print(f"\nВсего в коллекции: {len(collection)} квартир")

    # ──────────────────────────────────────────────────────────────────────
    # 4. Получение всех элементов
    # ──────────────────────────────────────────────────────────────────────
    print("\n4. Получение всех элементов из коллекции")
    print("-" * 70)

    all_apartments: List[Apartment] = collection.get_all()
    print(f"Получено элементов: {len(all_apartments)}")
    print(f"Тип возвращаемого значения: List[Apartment]")

    print("\nСписок всех квартир:")
    for i, apt in enumerate(all_apartments, 1):
        print(f"{i}. {apt}")
        print(f"   Цена за м²: {apt.price_per_sqm():.2f} руб.")

    # ──────────────────────────────────────────────────────────────────────
    # 5. Итерация по типизированной коллекции
    # ──────────────────────────────────────────────────────────────────────
    print("\n5. Итерация по коллекции")
    print("-" * 70)

    print("\nПеребор через for:")
    apartment: Apartment  # Аннотация типа для переменной цикла
    for apartment in collection:
        print(f"  - {apartment.address}: {apartment.price:,} руб.")

    # ──────────────────────────────────────────────────────────────────────
    # 6. Демонстрация типобезопасности
    # ──────────────────────────────────────────────────────────────────────
    print("\n6. Демонстрация типобезопасности")
    print("-" * 70)

    print("\nТипы известны на этапе написания кода:")
    print("  - IDE может подсказывать методы объектов")
    print("  - Статические анализаторы (mypy) могут проверять типы")

    # Пример: вызов методов с гарантией типа
    first_apartment: Apartment = all_apartments[0]
    price_per_sqm: float = first_apartment.price_per_sqm()
    print(f"\nПервая квартира: {first_apartment.address}")
    print(f"Цена за м²: {price_per_sqm:.2f} руб. (тип: float)")

    # ──────────────────────────────────────────────────────────────────────
    # 7. Использование метода find
    # ──────────────────────────────────────────────────────────────────────
    print("\n7. Поиск элемента по условию")
    print("-" * 70)

    # Находим дешёвую квартиру
    cheap: Optional[Apartment] = collection.find(lambda apt: apt.price < 30000)
    if cheap:
        print(f"Найдена дешёвая квартира: {cheap}")
    else:
        print("Дешёвых квартир не найдено")

    # Находим просторную квартиру
    spacious: Optional[Apartment] = collection.find(lambda apt: apt.area > 90)
    if spacious:
        print(f"Найдена просторная квартира: {spacious}")
    else:
        print("Просторных квартир не найдено")

    # ──────────────────────────────────────────────────────────────────────
    # 8. Удаление элемента
    # ──────────────────────────────────────────────────────────────────────
    print("\n8. Удаление элемента из коллекции")
    print("-" * 70)

    print(f"До удаления: {len(collection)} квартир")
    print(f"Удаляем: {apt2.address}")

    collection.remove(apt2)
    print(f"После удаления: {len(collection)} квартир")

    # ──────────────────────────────────────────────────────────────────────
    # 9. Работа с типами в функциях
    # ──────────────────────────────────────────────────────────────────────
    print("\n9. Функции с аннотациями типов")
    print("-" * 70)

    def calculate_average_price(apartments: List[Apartment]) -> float:
        """
        Вычисляет среднюю цену квартир.
        
        Args:
            apartments: список квартир
            
        Returns:
            средняя цена
        """
        if not apartments:
            return 0.0
        total: float = sum(apt.price for apt in apartments)
        return total / len(apartments)

    def find_expensive(apartments: List[Apartment], threshold: float) -> List[Apartment]:
        """
        Находит дорогие квартиры.
        
        Args:
            apartments: список квартир
            threshold: порог цены
            
        Returns:
            список дорогих квартир
        """
        return [apt for apt in apartments if apt.price > threshold]

    avg_price: float = calculate_average_price(collection.get_all())
    print(f"\nСредняя цена: {avg_price:,.2f} руб.")

    expensive: List[Apartment] = find_expensive(collection.get_all(), 50000)
    print(f"Дорогих квартир (>50000): {len(expensive)}")
    for apt in expensive:
        print(f"  - {apt.address}: {apt.price:,} руб.")

    # ──────────────────────────────────────────────────────────────────────
    # ИТОГ
    # ──────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("ИТОГ")
    print("=" * 70)

    print("\nРеализовано:")
    print("  ✓ Аннотации типов в классе Apartment")
    print("  ✓ Generic-класс TypedCollection[T]")
    print("  ✓ Типизированные методы коллекции")
    print("  ✓ Аннотации во всех функциях")
    print("  ✓ Использование TypeVar, Generic, List, Optional")

    print("\nПреимущества типизации:")
    print("  ✓ Автодополнение в IDE")
    print("  ✓ Раннее обнаружение ошибок")
    print("  ✓ Лучшая документация кода")
    print("  ✓ Упрощение рефакторинга")

    print(f"\nВсего создано квартир: {Apartment.get_total_count()}")
    print(f"В коллекции: {len(collection)}")

    print("\nДемонстрация завершена.")
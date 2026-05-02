"""
Демонстрационный скрипт для класса Apartment.
Предметная область: Недвижимость.

Сценарии:
    1. Создание объектов, __str__, __repr__, __eq__
    2. Работа с setter и атрибутом класса
    3. Бизнес-методы
    4. Демонстрация валидации (некорректные данные)
"""

import sys
import os

# Добавляем директорию lab01 в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import Apartment


def separator(title: str) -> None:
    """Вспомогательная функция: выводит заголовок секции."""
    print("\n" + "═" * 52)
    print(f"  {title}")
    print("═" * 52)


# ══════════════════════════════════════════════════════
#  СЦЕНАРИЙ 1 — Создание объектов и магические методы
# ══════════════════════════════════════════════════════
separator("СЦЕНАРИЙ 1: Создание объектов")

apt1 = Apartment(
    address="ул. Ленина, д. 10, кв. 5",
    area=54.5,
    price=35_000,
    rooms=2,
)
apt2 = Apartment(
    address="пр. Мира, д. 3, кв. 12",
    area=80.0,
    price=55_000,
    rooms=3,
)
# Квартира с тем же адресом и площадью, что и apt1
apt3 = Apartment(
    address="ул. Ленина, д. 10, кв. 5",
    area=54.5,
    price=40_000,
    rooms=2,
)

print("\n── Вывод через __str__ (print) ──")
print(apt1)
print()
print(apt2)

print("\n── Вывод через __repr__ ──")
print(repr(apt1))
print(repr(apt2))

print("\n── Сравнение объектов через __eq__ ──")
print(f"apt1 == apt2  : {apt1 == apt2}")   # False
print(f"apt1 == apt3  : {apt1 == apt3}")   # True
print(f"apt1 == 'str' : {apt1 == 'str'}") # NotImplemented → False

# ══════════════════════════════════════════════════════
#  СЦЕНАРИЙ 2 — Setter и атрибут класса
# ══════════════════════════════════════════════════════
separator("СЦЕНАРИЙ 2: Setter и атрибут класса")

print(f"\nЦена apt1 до изменения : {apt1.price:,.0f} руб.")
apt1.price = 42_000
print(f"Цена apt1 после setter : {apt1.price:,.0f} руб.")

print("\n── Проверка ограничений setter ──")
try:
    apt1.price = -500
except ValueError as e:
    print(f"ValueError (price = -500)       : {e}")

try:
    apt1.price = 2_000_000
except ValueError as e:
    print(f"ValueError (price = 2 000 000)  : {e}")

try:
    apt1.price = "бесплатно"
except TypeError as e:
    print(f"TypeError  (price = 'бесплатно'): {e}")

print("\n── Атрибут класса _total_count ──")
print(f"Через класс     : Apartment.get_total_count() = "
      f"{Apartment.get_total_count()}")
print(f"Через экземпляр : apt1.get_total_count()       = "
      f"{apt1.get_total_count()}")
print(f"Допустимые статусы (класс)    : "
      f"{Apartment.AVAILABLE_STATUSES}")
print(f"Допустимые статусы (экземпляр): "
      f"{apt1.AVAILABLE_STATUSES}")

# ══════════════════════════════════════════════════════
#  СЦЕНАРИЙ 3 — Бизнес-методы
# ══════════════════════════════════════════════════════
separator("СЦЕНАРИЙ 3: Бизнес-методы")

print(f"\nКвартира : {apt2.address}")
print(f"Площадь  : {apt2.area:.1f} м²")
print(f"Цена/мес : {apt2.price:,.0f} руб.")

ppsm         = apt2.price_per_sqm()
cost_default = apt2.monthly_cost_with_tax()
cost_20      = apt2.monthly_cost_with_tax(tax_rate=0.20)

print(f"\nЦена за 1 м²           : {ppsm:>10,.2f} руб./м²")
print(f"Цена с налогом 13%     : {cost_default:>10,.2f} руб.")
print(f"Цена с налогом 20%     : {cost_20:>10,.2f} руб.")

print("\n── Проверка ограничений monthly_cost_with_tax ──")
try:
    apt2.monthly_cost_with_tax(tax_rate=1.5)
except ValueError as e:
    print(f"ValueError (tax_rate=1.5)   : {e}")

try:
    apt2.monthly_cost_with_tax(tax_rate="много")
except TypeError as e:
    print(f"TypeError  (tax_rate='много'): {e}")

# ══════════════════════════════════════════════════════
#  СЦЕНАРИЙ 4 — Некорректное создание объектов
# ══════════════════════════════════════════════════════
separator("СЦЕНАРИЙ 4: Валидация при создании")

test_cases = [
    {
        "desc": "Пустой адрес",
        "kwargs": dict(address="", area=50.0,
                       price=20_000, rooms=2),
    },
    {
        "desc": "Адрес короче 5 символов",
        "kwargs": dict(address="ул.1", area=50.0,
                       price=20_000, rooms=2),
    },
    {
        "desc": "Адрес не строка (int)",
        "kwargs": dict(address=123, area=50.0,
                       price=20_000, rooms=2),
    },
    {
        "desc": "Отрицательная площадь",
        "kwargs": dict(address="ул. Пушкина, д. 1", area=-10.0,
                       price=20_000, rooms=2),
    },
    {
        "desc": "Площадь > 10 000 м²",
        "kwargs": dict(address="ул. Пушкина, д. 1", area=15_000.0,
                       price=20_000, rooms=2),
    },
    {
        "desc": "Отрицательная цена",
        "kwargs": dict(address="ул. Пушкина, д. 1", area=50.0,
                       price=-100, rooms=2),
    },
    {
        "desc": "Комнат = 0",
        "kwargs": dict(address="ул. Пушкина, д. 1", area=50.0,
                       price=20_000, rooms=0),
    },
    {
        "desc": "Комнат = 25 (> 20)",
        "kwargs": dict(address="ул. Пушкина, д. 1", area=50.0,
                       price=20_000, rooms=25),
    },
    {
        "desc": "Комнат — не int (float)",
        "kwargs": dict(address="ул. Пушкина, д. 1", area=50.0,
                       price=20_000, rooms=2.5),
    },
]

for case in test_cases:
    print(f"\n▶ {case['desc']}")
    try:
        obj = Apartment(**case["kwargs"])
        print(f"  Создан: {repr(obj)}")
    except (TypeError, ValueError) as e:
        print(f"  {type(e).__name__}: {e}")

# ══════════════════════════════════════════════════════
#  ИТОГ
# ══════════════════════════════════════════════════════
separator("ИТОГ")
print(f"\nВсего создано объектов Apartment: {Apartment.get_total_count()}")
print("\nДемонстрация завершена успешно.")
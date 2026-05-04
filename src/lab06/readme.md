# ЛР-6 — Generics и typing

## Предметная область

**Недвижимость** — типизированная система управления квартирами.

## Цель работы

Освоение системы аннотаций типов в Python и создание обобщённых (generic) классов с использованием модуля `typing`.

---

## Структура файлов
lab06/
├── README.md # Описание лабораторной работы
├── container.py # Generic-класс TypedCollection[T]
└── demo.py # Демонстрация типизации

---

## Реализованные компоненты

### 1. Apartment с полными аннотациями типов

Класс из ЛР-1, дополненный аннотациями типов для всех:
- параметров конструктора
- атрибутов экземпляра
- возвращаемых значений методов
- свойств (properties)

**Пример аннотаций:**

```python
class Apartment:
    AVAILABLE_STATUSES: tuple = ("available", "rented", "reserved")
    _total_count: int = 0

    def __init__(
        self,
        address: str,
        area: float,
        price: float,
        rooms: int,
    ) -> None:
        self._address: str = address
        self._area: float = float(area)
        self._price: float = float(price)
        self._rooms: int = rooms

    @property
    def address(self) -> str:
        return self._address

    def price_per_sqm(self) -> float:
        return self._price / self._area
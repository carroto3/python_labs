"""
Модуль консольного интерфейса (CLI) приложения «Недвижимость».
ОТВЕЧАЕТ ТОЛЬКО за ввод и вывод. Вся бизнес-логика — через app.ApartmentManager.
"""

import sys
import os as _os
from typing import List, Optional

# Добавляем путь к lab07 для импорта
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from models import Apartment, ResidentialApartment, CommercialApartment
from app import ApartmentManager
from exceptions import (
    RealEstateError,
    ItemNotFoundError,
    DuplicateItemError,
    ValidationError,
    StorageError,
)
from storage import Storage

# Путь к файлу данных по умолчанию
DEFAULT_DATA_FILE = _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)),
    "real_estate_data.json",
)

# Строки-разделители
_SEP = "─" * 85
_SEP_THIN = "─" * 60


class CLI:
    """Консольный интерфейс приложения «Недвижимость».

    Реализует интерактивное меню с операциями над коллекцией.
    НЕ обращается к коллекции напрямую — только через ApartmentManager.
    """

    def __init__(self, data_file: Optional[str] = None) -> None:
        filepath = data_file or DEFAULT_DATA_FILE
        self._storage = Storage(filepath)
        self._manager = ApartmentManager(storage=self._storage)

    # ==================================================================
    # Главный цикл
    # ==================================================================

    def run(self) -> None:
        """Главный цикл приложения."""
        self._print_header()

        # Загрузка данных
        try:
            self._manager.load()
            print(f"\n  Данные загружены. Объектов в коллекции: {self._manager.count}")
            if self._manager.count > 0:
                print("  (загружены демонстрационные данные)")
        except StorageError as e:
            print(f"\n  [!] {e}")
            print("  Начинаем с пустой коллекции.")

        while True:
            self._show_menu()
            choice = self._input_choice()

            if choice == 0:
                self._handle_exit()
                break
            elif choice == 1:
                self._handle_add()
            elif choice == 2:
                self._handle_show_all()
            elif choice == 3:
                self._handle_search()
            elif choice == 4:
                self._handle_filter()
            elif choice == 5:
                self._handle_delete()
            elif choice == 6:
                self._handle_save()
            elif choice == 7:
                self._handle_load()
            elif choice == 8:
                self._handle_demo()
            else:
                print("\n  [!] Неверный пункт меню. Попробуйте снова.")

    # ==================================================================
    # Меню и ввод
    # ==================================================================

    def _print_header(self) -> None:
        print("\n" + "=" * 85)
        print("  НЕДВИЖИМОСТЬ — консольное приложение для управления объектами")
        print("=" * 85)

    def _show_menu(self) -> None:
        print(f"\n{_SEP}")
        print("  ГЛАВНОЕ МЕНЮ")
        print(_SEP)
        print("  1. Добавить объект недвижимости")
        print("  2. Показать все объекты")
        print("  3. Найти объект по атрибуту")
        print("  4. Фильтровать объекты")
        print("  5. Удалить объект")
        print("  6. Сохранить данные в файл")
        print("  7. Загрузить данные из файла")
        print("  8. Сбросить к демо-данным")
        print("  0. Выход")
        print(_SEP)

    def _input_choice(self) -> int:
        """Запрашивает выбор пункта меню с обработкой некорректного ввода."""
        try:
            choice = int(input("\n  Выберите пункт: "))
        except ValueError:
            print("  [!] Ошибка: введите число.")
            return -1
        return choice

    # ==================================================================
    # 1. Добавление объекта
    # ==================================================================

    def _handle_add(self) -> None:
        print(f"\n{_SEP_THIN}")
        print("  ДОБАВЛЕНИЕ ОБЪЕКТА НЕДВИЖИМОСТИ")
        print(_SEP_THIN)

        # Выбор типа
        print("\n  Типы объектов:")
        for key, (desc, _) in self._manager.get_type_options().items():
            print(f"    {key} — {desc}")
        type_code = input("\n  Выберите тип (1-3, по умолчанию 1): ").strip()
        if type_code not in ("1", "2", "3"):
            type_code = "1"

        # Адрес
        address = input("  Адрес: ").strip()
        if not address:
            print("  [!] Адрес не может быть пустым.")
            return

        # Площадь
        try:
            area_raw = input("  Площадь (кв.м.): ").strip()
            area = self._manager.validate_float(area_raw, "Площадь")
            if area <= 0:
                print("  [!] Площадь должна быть положительной.")
                return
        except ValidationError as e:
            print(f"  [!] {e}")
            return

        # Цена
        try:
            price_raw = input("  Цена (руб.): ").strip()
            price = self._manager.validate_float(price_raw, "Цена")
            if price < 0:
                print("  [!] Цена не может быть отрицательной.")
                return
        except ValidationError as e:
            print(f"  [!] {e}")
            return

        # Комнаты
        try:
            rooms_raw = input("  Количество комнат: ").strip()
            rooms = self._manager.validate_int(rooms_raw, "Комнаты")
            if rooms <= 0:
                print("  [!] Количество комнат должно быть положительным.")
                return
        except ValidationError as e:
            print(f"  [!] {e}")
            return

        # Статус
        print("  Статусы: доступна / продана / забронирована")
        status = input("  Статус (по умолчанию 'доступна'): ").strip()
        if status not in ("доступна", "продана", "забронирована"):
            status = "доступна"

        # Дополнительные поля
        extra = {}
        if type_code == "2":  # ResidentialApartment
            try:
                floor_raw = input("  Этаж: ").strip()
                extra["floor"] = int(floor_raw) if floor_raw else 1
            except ValueError:
                print("  [!] Некорректный этаж. Установлен 1.")
                extra["floor"] = 1
            balcony = input("  Есть балкон? (да/нет, по умолчанию 'нет'): ").strip().lower()
            extra["has_balcony"] = balcony in ("да", "yes", "y", "1")

        elif type_code == "3":  # CommercialApartment
            print("  Типы бизнеса: офис / склад / магазин / салон / кафе")
            bt = input("  Тип бизнеса (по умолчанию 'офис'): ").strip()
            extra["business_type"] = bt if bt in ("офис", "склад", "магазин", "салон", "кафе") else "офис"
            parking = input("  Есть парковка? (да/нет, по умолчанию 'нет'): ").strip().lower()
            extra["has_parking"] = parking in ("да", "yes", "y", "1")

        # Добавление
        try:
            item = self._manager.add_apartment(
                type_code=type_code,
                address=address,
                area=area,
                price=price,
                rooms=rooms,
                status=status,
                **extra,
            )
            print(f"\n  [OK] Объект добавлен:")
            print(f"  {item.to_string()}")
        except (ValidationError, ValueError) as e:
            print(f"\n  [!] Ошибка: {e}")

    # ==================================================================
    # 2. Показать все объекты
    # ==================================================================

    def _handle_show_all(self) -> None:
        print(f"\n{_SEP_THIN}")
        print("  ВСЕ ОБЪЕКТЫ НЕДВИЖИМОСТИ")
        print(_SEP_THIN)
        items = self._manager.get_all()
        if not items:
            print("\n  Коллекция пуста.")
            return
        print(f"\n  Всего объектов: {len(items)}\n")
        self._print_table(items)

    # ==================================================================
    # 3. Поиск по атрибуту
    # ==================================================================

    def _handle_search(self) -> None:
        print(f"\n{_SEP_THIN}")
        print("  ПОИСК ОБЪЕКТА ПО АТРИБУТУ")
        print(_SEP_THIN)

        attrs = self._manager.get_searchable_attributes()
        print("\n  Доступные атрибуты:")
        for a in attrs:
            print(f"    • {a}")
        print("\n  (поиск без учёта регистра)")

        attr = input("\n  Введите атрибут: ").strip().lower()
        if not attr:
            print("  [!] Атрибут не может быть пустым.")
            return

        value = input("  Введите значение: ").strip()
        if not value:
            print("  [!] Значение не может быть пустым.")
            return

        try:
            results = self._manager.find_by_attribute(attr, value)
        except ValidationError as e:
            print(f"\n  [!] {e}")
            return

        if not results:
            print(f"\n  Объекты с '{attr}' = '{value}' не найдены.")
            return

        print(f"\n  Найдено объектов: {len(results)}\n")
        self._print_table(results)

    # ==================================================================
    # 4. Фильтрация (подменю)
    # ==================================================================

    def _handle_filter(self) -> None:
        while True:
            print(f"\n{_SEP_THIN}")
            print("  ФИЛЬТРАЦИЯ ОБЪЕКТОВ")
            print(_SEP_THIN)
            print("  1. По диапазону цен")
            print("  2. По диапазону площади")
            print("  3. По количеству комнат")
            print("  4. По статусу")
            print("  5. По типу (обычная / жилая / коммерческая)")
            print("  6. По произвольному условию (демо)")
            print("  0. Назад")
            print(_SEP_THIN)

            choice = self._input_choice()
            if choice == 0:
                break
            elif choice == 1:
                self._filter_price()
            elif choice == 2:
                self._filter_area()
            elif choice == 3:
                self._filter_rooms()
            elif choice == 4:
                self._filter_status()
            elif choice == 5:
                self._filter_type()
            elif choice == 6:
                self._filter_custom()
            else:
                print("\n  [!] Неверный пункт.")

    def _filter_price(self) -> None:
        print("\n  Фильтр по диапазону цен")
        try:
            min_p = float(input("  Минимальная цена (руб.): "))
            max_p = float(input("  Максимальная цена (руб.): "))
        except ValueError:
            print("  [!] Некорректное значение.")
            return
        results = self._manager.filter_by_price_range(min_p, max_p)
        self._show_filter_results(results, f"цене от {min_p:,.0f} до {max_p:,.0f} руб.")

    def _filter_area(self) -> None:
        print("\n  Фильтр по диапазону площади")
        try:
            min_a = float(input("  Минимальная площадь (кв.м.): "))
            max_a = float(input("  Максимальная площадь (кв.м.): "))
        except ValueError:
            print("  [!] Некорректное значение.")
            return
        results = self._manager.filter_by_area_range(min_a, max_a)
        self._show_filter_results(results, f"площади от {min_a} до {max_a} кв.м.")

    def _filter_rooms(self) -> None:
        print("\n  Фильтр по количеству комнат")
        try:
            rooms = int(input("  Количество комнат: "))
        except ValueError:
            print("  [!] Некорректное значение.")
            return
        results = self._manager.filter_by_rooms(rooms)
        self._show_filter_results(results, f"количеству комнат = {rooms}")

    def _filter_status(self) -> None:
        print("\n  Фильтр по статусу")
        print("  Доступные статусы: доступна / продана / забронирована")
        status = input("  Статус: ").strip()
        if status not in ("доступна", "продана", "забронирована"):
            print("  [!] Некорректный статус.")
            return
        results = self._manager.filter_by_status(status)
        self._show_filter_results(results, f"статусу '{status}'")

    def _filter_type(self) -> None:
        print("\n  Фильтр по типу объекта")
        print("  1 — Обычная квартира (Apartment)")
        print("  2 — Жилая квартира (ResidentialApartment)")
        print("  3 — Коммерческая недвижимость (CommercialApartment)")
        tc = input("  Выберите тип: ").strip()
        type_map = {"1": Apartment, "2": ResidentialApartment, "3": CommercialApartment}
        cls = type_map.get(tc)
        if cls is None:
            print("  [!] Некорректный выбор.")
            return
        results = self._manager.filter_by_type(cls)
        self._show_filter_results(results, f"типу '{cls.__name__}'")

    def _filter_custom(self) -> None:
        print("\n  Демонстрация произвольного условия:")
        print("  'Жилые квартиры с балконом, площадью > 50 кв.м., ценой < 6 млн.'")
        results = self._manager.find_by_predicate(
            lambda a: (
                isinstance(a, ResidentialApartment)
                and a.has_balcony
                and a.area > 50
                and a.price < 6000000
            )
        )
        self._show_filter_results(
            results,
            "условию: жилая, с балконом, >50 кв.м., <6 млн."
        )

    def _show_filter_results(self, results: List[Apartment], condition: str) -> None:
        if not results:
            print(f"\n  Объектов по {condition} не найдено.")
            return
        print(f"\n  Найдено объектов по {condition}: {len(results)}\n")
        self._print_table(results)

    # ==================================================================
    # 5. Удаление
    # ==================================================================

    def _handle_delete(self) -> None:
        print(f"\n{_SEP_THIN}")
        print("  УДАЛЕНИЕ ОБЪЕКТА")
        print(_SEP_THIN)
        try:
            item_id = int(input("\n  Введите ID объекта для удаления: "))
        except ValueError:
            print("  [!] Ошибка: введите число.")
            return

        try:
            removed = self._manager.remove_by_id(item_id)
            print(f"\n  [OK] Объект удалён: {removed.to_short_string()}")
        except ItemNotFoundError as e:
            print(f"\n  [!] {e}")

    # ==================================================================
    # 6. Сохранение
    # ==================================================================

    def _handle_save(self) -> None:
        print(f"\n{_SEP_THIN}")
        print("  СОХРАНЕНИЕ ДАННЫХ")
        print(_SEP_THIN)
        try:
            self._manager.save()
            print(f"\n  [OK] Данные сохранены в '{self._storage.filepath}'.")
            print(f"  Сохранено объектов: {self._manager.count}")
        except StorageError as e:
            print(f"\n  [!] {e}")

    # ==================================================================
    # 7. Загрузка
    # ==================================================================

    def _handle_load(self) -> None:
        print(f"\n{_SEP_THIN}")
        print("  ЗАГРУЗКА ДАННЫХ")
        print(_SEP_THIN)
        try:
            self._manager.load()
            print(f"\n  [OK] Данные загружены из '{self._storage.filepath}'.")
            print(f"  Загружено объектов: {self._manager.count}")
        except StorageError as e:
            print(f"\n  [!] {e}")

    # ==================================================================
    # 8. Демо-данные
    # ==================================================================

    def _handle_demo(self) -> None:
        """Сброс к демонстрационным данным."""
        self._manager.reset_to_demo()
        print(f"\n  [OK] Загружены демонстрационные данные.")
        print(f"  Объектов: {self._manager.count}")

    # ==================================================================
    # Выход
    # ==================================================================

    def _handle_exit(self) -> None:
        print(f"\n{_SEP_THIN}")
        print("  ВЫХОД")
        print(_SEP_THIN)
        try:
            ans = input("\n  Сохранить данные перед выходом? (y/n): ").strip().lower()
            if ans in ("y", "yes", "д", "да", ""):
                self._manager.save()
                print(f"  [OK] Данные сохранены. Всего объектов: {self._manager.count}")
        except StorageError as e:
            print(f"  [!] {e}")
        print("\n  До свидания!\n")

    # ==================================================================
    # Форматированный табличный вывод
    # ==================================================================

    @staticmethod
    def _print_table(items: List[Apartment]) -> None:
        """Выводит список объектов в виде форматированной таблицы."""
        if not items:
            print("  Нет данных.")
            return

        # Заголовок
        header = (
            f"  {'ID':<5} {'Тип':<10} {'Адрес':<28} "
            f"{'Площадь':<8} {'Комн':<5} {'Цена':<14} {'Статус':<14} {'Доп. инфо'}"
        )
        print(header)
        print("  " + "─" * (len(header) - 2))

        for item in items:
            item_type = type(item).__name__
            # Базовые поля
            line = (
                f"  {item.id:<5} {item_type:<10} "
                f"{_truncate(item.address, 28):<28} "
                f"{item.area:<8.1f} {item.rooms:<5} "
                f"{item.price:<14,.0f} {item.status:<14}"
            )
            # Доп. инфо
            if isinstance(item, ResidentialApartment):
                balcony = "балкон" if item.has_balcony else "без балк."
                line += f" {item.floor} эт., {balcony}"
            elif isinstance(item, CommercialApartment):
                parking = "парковка" if item.has_parking else "без парк."
                line += f" {item.business_type}, {parking}"
            print(line)


def _truncate(text: str, max_len: int) -> str:
    """Обрезает строку до max_len символов."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."

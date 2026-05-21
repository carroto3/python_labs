"""
Модуль интерфейса командной строки (CLI).
Предметная область: Недвижимость.

Обеспечивает отображение интерактивного меню, приём ввода от пользователя
и форматированный вывод результатов. Не содержит бизнес-логики —
все операции выполняются через слой app.py (ApartmentService).

Реализует:
    - 10 пунктов меню (просмотр, добавление, удаление, поиск,
      фильтрация, сортировка, статистика, сохранение, загрузка, выход).
    - Обработку некорректного ввода (строки вместо чисел, выход за диапазон).
    - Форматированный табличный вывод объектов.
    - Подтверждение опасных операций (удаление).
    - Автосохранение при выходе.
"""

from typing import Optional

from app import ApartmentService
from models import (
    Apartment,
    ResidentialApartment,
    CommercialApartment,
)
from exceptions import (
    ItemNotFoundError,
    DuplicateItemError,
    StorageError,
)


class CLI:
    """
    Интерфейс командной строки для управления недвижимостью.

    Принимает сервис бизнес-логики (ApartmentService) и предоставляет
    интерактивное меню с операциями над коллекцией.
    CLI не обращается к коллекции напрямую — только через сервис.

    Attributes:
        _service (ApartmentService): сервис бизнес-логики.
        _data_file (str): путь к JSON-файлу для сохранения/загрузки данных.
    """

    def __init__(
        self, service: ApartmentService, data_file: str = "data.json"
    ) -> None:
        """
        Инициализирует CLI с указанным сервисом и путём к файлу данных.

        Args:
            service: экземпляр ApartmentService с бизнес-логикой.
            data_file: путь к файлу для автоматического сохранения/загрузки.
        """
        self._service: ApartmentService = service
        self._data_file: str = data_file

    # ── Главный цикл ────────────────────────────────────────────────────

    def run(self) -> None:
        """
        Запускает главный цикл CLI.

        В бесконечном цикле отображает меню, принимает выбор пользователя
        и вызывает соответствующий обработчик. Цикл прерывается только
        при выборе пункта «Выход» (10).
        """
        while True:
            self._print_menu()
            choice: Optional[int] = self._read_int(
                "\nВыберите пункт меню: ", min_val=1, max_val=10
            )
            if choice is None:
                continue

            if choice == 1:
                self._handle_show_all()
            elif choice == 2:
                self._handle_add()
            elif choice == 3:
                self._handle_remove()
            elif choice == 4:
                self._handle_search()
            elif choice == 5:
                self._handle_filter()
            elif choice == 6:
                self._handle_sort()
            elif choice == 7:
                self._handle_statistics()
            elif choice == 8:
                self._handle_save()
            elif choice == 9:
                self._handle_load()
            elif choice == 10:
                self._handle_exit()
                break

    # ── Отображение меню ────────────────────────────────────────────────

    @staticmethod
    def _print_menu() -> None:
        """Выводит главное меню приложения с нумерованными пунктами."""
        print()
        print("=" * 60)
        print("  СИСТЕМА УПРАВЛЕНИЯ НЕДВИЖИМОСТЬЮ")
        print("=" * 60)
        print("  1. Показать все объекты")
        print("  2. Добавить объект")
        print("  3. Удалить объект")
        print("  4. Поиск по атрибуту")
        print("  5. Фильтрация по условию")
        print("  6. Сортировка")
        print("  7. Статистика")
        print("  8. Сохранить данные")
        print("  9. Загрузить данные")
        print(" 10. Выход")
        print("-" * 60)

    # ── Обработчики пунктов меню ────────────────────────────────────────

    def _handle_show_all(self) -> None:
        """
        Обрабатывает пункт 1: «Показать все объекты».

        Выводит все объекты коллекции в форматированной таблице.
        Если коллекция пуста, выводит информационное сообщение.
        """
        items: list[Apartment] = self._service.get_all()
        if not items:
            print("\nКоллекция пуста. Добавьте объекты через пункт 2.")
            return
        print(f"\nВсего объектов в коллекции: {len(items)}")
        self._print_table(items)

    def _handle_add(self) -> None:
        """
        Обрабатывает пункт 2: «Добавить объект».

        Предлагает выбрать тип создаваемого объекта (обычная квартира,
        жилая квартира или коммерческое помещение), запрашивает
        необходимые атрибуты и добавляет объект в коллекцию.

        Перехватывает DuplicateItemError при попытке добавить дубликат,
        а также TypeError/ValueError при некорректных входных данных.
        """
        print("\n--- Добавление нового объекта ---")
        print("Типы объектов:")
        print("  1. Обычная квартира (Apartment)")
        print("  2. Жилая квартира (ResidentialApartment)")
        print("  3. Коммерческое помещение (CommercialApartment)")

        type_choice: Optional[int] = self._read_int(
            "Выберите тип объекта (1-3): ", min_val=1, max_val=3
        )
        if type_choice is None:
            return

        try:
            if type_choice == 1:
                item: Apartment = self._input_apartment()
            elif type_choice == 2:
                item = self._input_residential()
            else:
                item = self._input_commercial()

            self._service.add(item)
            print(f"\nОбъект успешно добавлен!")
            print(f"  ID: {item.id[:8]}...")
            print(f"  Тип: {type(item).__name__}")
            print(f"  Адрес: {item.address}")
        except DuplicateItemError as exc:
            print(f"\nОшибка: {exc}")
        except (TypeError, ValueError) as exc:
            print(f"\nОшибка ввода: {exc}")

    def _input_apartment(self) -> Apartment:
        """
        Запрашивает у пользователя данные для создания обычной квартиры.

        Returns:
            Apartment: новый объект квартиры.

        Raises:
            ValueError: если какое-либо из введённых значений некорректно.
        """
        print("\nВведите данные квартиры:")
        address: str = self._read_str(
            "  Адрес (мин. 5 символов): ", min_len=5
        )
        area: Optional[float] = self._read_float(
            "  Площадь (м², 1-10000): ", min_val=1, max_val=10000
        )
        if area is None:
            raise ValueError("Некорректная площадь")
        price: Optional[float] = self._read_float(
            "  Цена аренды (руб./мес, 0-1000000): ",
            min_val=0, max_val=1000000,
        )
        if price is None:
            raise ValueError("Некорректная цена")
        rooms: Optional[int] = self._read_int(
            "  Количество комнат (1-20): ", min_val=1, max_val=20
        )
        if rooms is None:
            raise ValueError("Некорректное количество комнат")
        status: str = self._read_status()
        return Apartment(
            address=address, area=area, price=price,
            rooms=rooms, status=status,
        )

    def _input_residential(self) -> ResidentialApartment:
        """
        Запрашивает у пользователя данные для создания жилой квартиры.

        Returns:
            ResidentialApartment: новый объект жилой квартиры.

        Raises:
            ValueError: если какое-либо из введённых значений некорректно.
        """
        print("\nВведите данные жилой квартиры:")
        address: str = self._read_str(
            "  Адрес (мин. 5 символов): ", min_len=5
        )
        area: Optional[float] = self._read_float(
            "  Площадь (м², 1-10000): ", min_val=1, max_val=10000
        )
        if area is None:
            raise ValueError("Некорректная площадь")
        price: Optional[float] = self._read_float(
            "  Цена аренды (руб./мес, 0-1000000): ",
            min_val=0, max_val=1000000,
        )
        if price is None:
            raise ValueError("Некорректная цена")
        rooms: Optional[int] = self._read_int(
            "  Количество комнат (1-20): ", min_val=1, max_val=20
        )
        if rooms is None:
            raise ValueError("Некорректное количество комнат")
        has_balcony: bool = self._read_bool(
            "  Наличие балкона (y/n): "
        )
        floor: Optional[int] = self._read_int(
            "  Этаж (1-200): ", min_val=1, max_val=200
        )
        if floor is None:
            raise ValueError("Некорректный этаж")
        status: str = self._read_status()
        return ResidentialApartment(
            address=address, area=area, price=price, rooms=rooms,
            has_balcony=has_balcony, floor=floor, status=status,
        )

    def _input_commercial(self) -> CommercialApartment:
        """
        Запрашивает у пользователя данные для создания коммерческого помещения.

        Returns:
            CommercialApartment: новый объект коммерческого помещения.

        Raises:
            ValueError: если какое-либо из введённых значений некорректно.
        """
        print("\nВведите данные коммерческого помещения:")
        address: str = self._read_str(
            "  Адрес (мин. 5 символов): ", min_len=5
        )
        area: Optional[float] = self._read_float(
            "  Площадь (м², 1-10000): ", min_val=1, max_val=10000
        )
        if area is None:
            raise ValueError("Некорректная площадь")
        price: Optional[float] = self._read_float(
            "  Цена аренды (руб./мес, 0-1000000): ",
            min_val=0, max_val=1000000,
        )
        if price is None:
            raise ValueError("Некорректная цена")
        rooms: Optional[int] = self._read_int(
            "  Количество помещений (1-20): ", min_val=1, max_val=20
        )
        if rooms is None:
            raise ValueError("Некорректное количество помещений")
        print(
            "  Допустимые типы бизнеса: "
            f"{', '.join(CommercialApartment.VALID_BUSINESS_TYPES)}"
        )
        business_type: str = self._read_str(
            "  Тип бизнеса: ", min_len=2
        )
        has_parking: bool = self._read_bool(
            "  Наличие парковки (y/n): "
        )
        status: str = self._read_status()
        return CommercialApartment(
            address=address, area=area, price=price, rooms=rooms,
            business_type=business_type, has_parking=has_parking,
            status=status,
        )

    def _handle_remove(self) -> None:
        """
        Обрабатывает пункт 3: «Удалить объект».

        Выводит список объектов, запрашивает ID для удаления
        и требует подтверждения перед выполнением операции.
        Перехватывает ItemNotFoundError, если объект не найден.
        """
        items: list[Apartment] = self._service.get_all()
        if not items:
            print("\nКоллекция пуста. Нечего удалять.")
            return

        self._print_table(items)
        item_id: str = self._read_str(
            "\nВведите ID объекта для удаления: ", min_len=1
        )

        try:
            item: Optional[Apartment] = self._service.find_by_id(item_id)
            if item is None:
                raise ItemNotFoundError(item_id)

            # Подтверждение опасной операции
            print(f"\nВы собираетесь удалить:")
            print(f"  {item.to_short_string()}")
            confirmed: bool = self._read_bool(
                "Удалить этот объект? (y/n): "
            )
            if not confirmed:
                print("Удаление отменено.")
                return

            removed: Apartment = self._service.remove(item_id)
            print(
                f"\nОбъект успешно удалён: {removed.to_short_string()}"
            )
        except ItemNotFoundError as exc:
            print(f"\nОшибка: {exc}")

    def _handle_search(self) -> None:
        """
        Обрабатывает пункт 4: «Поиск по атрибуту».

        Позволяет искать объекты по атрибутам:
        address, status, rooms, type.
        Выводит результаты в форматированной таблице.
        """
        print("\n--- Поиск по атрибуту ---")
        print("Доступные атрибуты: address, status, rooms, type")
        attribute: str = self._read_str(
            "Введите атрибут для поиска: ", min_len=1
        )
        value: str = self._read_str(
            "Введите значение для поиска: ", min_len=1
        )

        try:
            results: list[Apartment] = (
                self._service.search_by_attribute(attribute, value)
            )
            if not results:
                print(
                    f"\nПо запросу '{attribute}={value}' "
                    f"ничего не найдено."
                )
            else:
                print(f"\nНайдено объектов: {len(results)}")
                self._print_table(results)
        except ValueError as exc:
            print(f"\nОшибка: {exc}")

    def _handle_filter(self) -> None:
        """
        Обрабатывает пункт 5: «Фильтрация по условию».

        Предлагает четыре типа фильтрации:
            1. По диапазону цен.
            2. По диапазону площади.
            3. По статусу.
            4. По типу (жилая / коммерческая).
        """
        print("\n--- Фильтрация по условию ---")
        print("  1. По диапазону цен")
        print("  2. По диапазону площади")
        print("  3. По статусу")
        print("  4. По типу (жилая / коммерческая)")

        filter_choice: Optional[int] = self._read_int(
            "Выберите тип фильтрации (1-4): ", min_val=1, max_val=4
        )
        if filter_choice is None:
            return

        try:
            results: list[Apartment] = []

            if filter_choice == 1:
                min_p: Optional[float] = self._read_float(
                    "  Минимальная цена: ", min_val=0
                )
                max_p: Optional[float] = self._read_float(
                    "  Максимальная цена: ", min_val=0
                )
                if min_p is not None and max_p is not None:
                    results = self._service.filter_by_price_range(
                        min_p, max_p
                    )

            elif filter_choice == 2:
                min_a: Optional[float] = self._read_float(
                    "  Минимальная площадь (м²): ", min_val=1
                )
                max_a: Optional[float] = self._read_float(
                    "  Максимальная площадь (м²): ", min_val=1
                )
                if min_a is not None and max_a is not None:
                    results = self._service.filter_by_area_range(
                        min_a, max_a
                    )

            elif filter_choice == 3:
                print(
                    "  Допустимые статусы: "
                    f"{', '.join(Apartment.AVAILABLE_STATUSES)}"
                )
                status: str = self._read_str(
                    "  Статус: ", min_len=1
                )
                results = self._service.filter_by_status(status)

            elif filter_choice == 4:
                obj_type: str = self._read_str(
                    "  Тип (residential/commercial "
                    "или жилая/коммерческая): ",
                    min_len=1,
                )
                results = self._service.filter_by_type(obj_type)

            if not results:
                print("\nПо заданному условию ничего не найдено.")
            else:
                print(f"\nНайдено объектов: {len(results)}")
                self._print_table(results)
        except ValueError as exc:
            print(f"\nОшибка: {exc}")

    def _handle_sort(self) -> None:
        """
        Обрабатывает пункт 6: «Сортировка».

        Предлагает выбор стратегии сортировки:
            1. По названию (адресу).
            2. По цене.
            3. По дате добавления.
            4. По площади.

        И выбор направления: по возрастанию или по убыванию.
        """
        print("\n--- Сортировка ---")
        print("Сортировать по:")
        print("  1. Названию (адресу)")
        print("  2. Цене")
        print("  3. Дате добавления")
        print("  4. Площади")

        sort_choice: Optional[int] = self._read_int(
            "Выберите стратегию сортировки (1-4): ",
            min_val=1, max_val=4,
        )
        if sort_choice is None:
            return

        print("Порядок сортировки:")
        print("  1. По возрастанию")
        print("  2. По убыванию")
        order_choice: Optional[int] = self._read_int(
            "Выберите порядок (1-2): ", min_val=1, max_val=2
        )
        if order_choice is None:
            return

        reverse: bool = (order_choice == 2)

        if sort_choice == 1:
            results: list[Apartment] = self._service.sort_by_address(
                reverse=reverse
            )
            label: str = "адресу"
        elif sort_choice == 2:
            results = self._service.sort_by_price(reverse=reverse)
            label = "цене"
        elif sort_choice == 3:
            results = self._service.sort_by_date_added(reverse=reverse)
            label = "дате добавления"
        else:
            results = self._service.sort_by_area(reverse=reverse)
            label = "площади"

        direction: str = "убыванию" if reverse else "возрастанию"
        print(
            f"\nОтсортировано по {label} (по {direction}):"
        )
        self._print_table(results)

    def _handle_statistics(self) -> None:
        """
        Обрабатывает пункт 7: «Статистика».

        Выводит сводную статистику по коллекции: количество объектов,
        среднюю/мин/макс цену, среднюю площадь, распределение
        по статусам и типам объектов.
        """
        stats: dict = self._service.get_statistics()
        print("\n--- Статистика коллекции ---")
        print(f"  Всего объектов:        {stats['total']}")
        print(f"  Средняя цена:          {stats['avg_price']:,.2f} руб.")
        print(f"  Средняя площадь:       {stats['avg_area']:,.2f} м²")
        print(f"  Минимальная цена:      {stats['min_price']:,.2f} руб.")
        print(f"  Максимальная цена:     {stats['max_price']:,.2f} руб.")

        if stats["statuses"]:
            print("  Статусы:")
            for s, count in stats["statuses"].items():
                print(f"    - {s}: {count}")

        if stats["types"]:
            print("  Типы объектов:")
            for t, count in stats["types"].items():
                print(f"    - {t}: {count}")

    def _handle_save(self) -> None:
        """
        Обрабатывает пункт 8: «Сохранить данные».

        Сохраняет текущую коллекцию в JSON-файл через storage.save().
        Перехватывает ошибки ввода-вывода.
        """
        from storage import save

        try:
            items: list[Apartment] = self._service.get_all()
            save(items, self._data_file)
            print(
                f"\nДанные успешно сохранены в файл "
                f"'{self._data_file}'."
            )
            print(f"Сохранено объектов: {len(items)}")
        except (IOError, StorageError) as exc:
            print(f"\nОшибка при сохранении: {exc}")

    def _handle_load(self) -> None:
        """
        Обрабатывает пункт 9: «Загрузить данные».

        Загружает коллекцию из JSON-файла через storage.load()
        и заменяет текущую коллекцию загруженными данными.
        Перехватывает ошибки отсутствия файла и повреждённых данных.
        """
        from storage import load

        try:
            items: list[Apartment] = load(self._data_file)
            self._service.set_items(items)
            print(
                f"\nДанные успешно загружены из файла "
                f"'{self._data_file}'."
            )
            print(f"Загружено объектов: {len(items)}")
        except FileNotFoundError:
            print(
                f"\nФайл данных '{self._data_file}' не найден."
            )
        except (IOError, ValueError, StorageError) as exc:
            print(f"\nОшибка при загрузке: {exc}")

    def _handle_exit(self) -> None:
        """
        Обрабатывает пункт 10: «Выход».

        Автоматически сохраняет данные перед выходом.
        Выводит прощальное сообщение.
        """
        from storage import save

        try:
            items: list[Apartment] = self._service.get_all()
            save(items, self._data_file)
            print(
                f"\nДанные автоматически сохранены в "
                f"'{self._data_file}'."
            )
        except (IOError, StorageError) as exc:
            print(
                f"\nПредупреждение: не удалось сохранить данные: {exc}"
            )
        print("\nВыход из программы. До свидания!")

    # ── Форматированный вывод ───────────────────────────────────────────

    @staticmethod
    def _print_table(items: list[Apartment]) -> None:
        """
        Выводит список объектов недвижимости в виде форматированной таблицы.

        Колонки: №, ID (первые 8 символов), Тип, Адрес, Площадь,
        Комнат, Цена, Статус, Дата добавления.

        Args:
            items: список объектов Apartment для отображения.
        """
        if not items:
            print("  (нет объектов)")
            return

        # Заголовок таблицы с фиксированной шириной колонок
        header: str = (
            f"{'№':>3}  {'ID':>10}  {'Тип':<20}  {'Адрес':<30}  "
            f"{'Площ.':>7}  {'Комн.':>5}  {'Цена':>12}  "
            f"{'Статус':<12}  {'Добавлен':<19}"
        )
        separator: str = "-" * len(header)

        print(f"\n{separator}")
        print(header)
        print(separator)

        for i, item in enumerate(items, 1):
            item_type: str = type(item).__name__
            # Обрезаем длинные строки для аккуратного табличного вывода
            row: str = (
                f"{i:>3}  {item.id[:8]:>10}  {item_type:<20}  "
                f"{item.address[:29]:<30}  "
                f"{item.area:>6.1f}  {item.rooms:>5}  "
                f"{item.price:>11,.0f}  "
                f"{item.status:<12}  {item.date_added[:19]:<19}"
            )
            print(row)

        print(separator)
        print(f"  Всего: {len(items)} объектов")

    # ── Вспомогательные методы ввода (только ввод-вывод) ────────────────

    @staticmethod
    def _read_int(
        prompt: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None,
    ) -> Optional[int]:
        """
        Считывает целое число от пользователя с проверкой диапазона.

        При некорректном вводе (строка вместо числа, выход за диапазон)
        выводит сообщение об ошибке и возвращает None.

        Args:
            prompt: строка-приглашение для ввода.
            min_val: минимальное допустимое значение (включительно).
            max_val: максимальное допустимое значение (включительно).

        Returns:
            Optional[int]: введённое число или None при ошибке.
        """
        try:
            value: int = int(input(prompt))
            if min_val is not None and value < min_val:
                print(
                    f"Ошибка: число должно быть не менее {min_val}."
                )
                return None
            if max_val is not None and value > max_val:
                print(
                    f"Ошибка: число должно быть не более {max_val}."
                )
                return None
            return value
        except ValueError:
            print("Ошибка: введите целое число.")
            return None

    @staticmethod
    def _read_float(
        prompt: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
    ) -> Optional[float]:
        """
        Считывает число с плавающей запятой от пользователя.

        При некорректном вводе выводит сообщение об ошибке
        и возвращает None.

        Args:
            prompt: строка-приглашение для ввода.
            min_val: минимальное допустимое значение.
            max_val: максимальное допустимое значение.

        Returns:
            Optional[float]: введённое число или None при ошибке.
        """
        try:
            value: float = float(input(prompt))
            if min_val is not None and value < min_val:
                print(
                    f"Ошибка: число должно быть не менее {min_val}."
                )
                return None
            if max_val is not None and value > max_val:
                print(
                    f"Ошибка: число должно быть не более {max_val}."
                )
                return None
            return value
        except ValueError:
            print("Ошибка: введите число.")
            return None

    @staticmethod
    def _read_str(prompt: str, min_len: int = 0) -> str:
        """
        Считывает непустую строку от пользователя.

        Повторяет запрос, пока не будет введена строка
        требуемой минимальной длины.

        Args:
            prompt: строка-приглашение для ввода.
            min_len: минимальная допустимая длина строки.

        Returns:
            str: введённая строка (без начальных/конечных пробелов).
        """
        while True:
            value: str = input(prompt).strip()
            if len(value) >= min_len:
                return value
            print(
                f"Ошибка: строка должна содержать "
                f"не менее {min_len} символов."
            )

    @staticmethod
    def _read_bool(prompt: str) -> bool:
        """
        Считывает ответ «да/нет» от пользователя.

        Принимает: y, yes, д, да, 1 — как True.
                   n, no, н, нет, 0 — как False.

        Args:
            prompt: строка-приглашение для ввода.

        Returns:
            bool: True при утвердительном ответе, False при отрицательном.
        """
        while True:
            value: str = input(prompt).strip().lower()
            if value in ("y", "yes", "д", "да", "1"):
                return True
            elif value in ("n", "no", "н", "нет", "0"):
                return False
            print("Ошибка: введите 'y' (да) или 'n' (нет).")

    @staticmethod
    def _read_status() -> str:
        """
        Запрашивает статус объекта с возможностью выбора из допустимых.

        Если пользователь вводит пустую строку, возвращает статус
        по умолчанию — 'available'.

        Returns:
            str: выбранный статус (один из Apartment.AVAILABLE_STATUSES).
        """
        print(
            f"  Допустимые статусы: "
            f"{', '.join(Apartment.AVAILABLE_STATUSES)}"
        )
        status: str = input(
            "  Статус (по умолчанию 'available'): "
        ).strip()
        if not status:
            return "available"
        return status

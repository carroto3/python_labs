"""
Точка входа в приложение системы управления недвижимостью.
Предметная область: Недвижимость.

При запуске автоматически загружает данные из JSON-файла (data.json),
расположенного рядом с main.py. При выходе данные автоматически
сохраняются в тот же файл.

Запуск:
    python main.py
"""

import os
import sys

from app import ApartmentService
from cli import CLI
from storage import load


def main() -> None:
    """
    Главная функция приложения.

    Выполняет:
        1. Определение пути к файлу данных (data.json рядом с main.py).
        2. Инициализацию сервиса бизнес-логики (ApartmentService).
        3. Автоматическую загрузку данных из JSON-файла при запуске.
        4. Запуск интерактивного CLI-цикла (CLI.run()).
           При выходе данные сохраняются автоматически.
    """
    # Определяем путь к файлу данных: data.json в той же папке, что и main.py
    data_file: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data.json"
    )

    # Инициализация сервиса бизнес-логики
    service: ApartmentService = ApartmentService()

    # Приветствие и информация о файле данных
    print("=" * 60)
    print("  СИСТЕМА УПРАВЛЕНИЯ НЕДВИЖИМОСТЬЮ")
    print("=" * 60)
    print(f"\nФайл данных: {data_file}")

    # Автозагрузка данных при запуске
    try:
        items = load(data_file)
        service.set_items(items)
        print(f"Автоматически загружено объектов: {len(items)}")
    except FileNotFoundError:
        print(
            "Файл данных не найден. Начинаем с пустой коллекции."
        )
    except (IOError, ValueError) as exc:
        print(
            f"Предупреждение: не удалось загрузить данные: {exc}"
        )
        print("Начинаем с пустой коллекции.")

    # Запуск интерактивного CLI
    # При выходе данные автоматически сохраняются в _handle_exit()
    cli: CLI = CLI(service, data_file)
    cli.run()


if __name__ == "__main__":
    main()

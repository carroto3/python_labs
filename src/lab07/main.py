"""
Точка входа в приложение «Недвижимость».
Запускает интерактивный консольный интерфейс (CLI).

Использование:
    python main.py                  — запуск с файлом данных по умолчанию.
    python main.py my_data.json     — запуск с указанным файлом.
"""

import sys
import os as _os

sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from cli import CLI


def main() -> None:
    """Главная функция. Запускает CLI-приложение."""
    data_file = sys.argv[1] if len(sys.argv) > 1 else None
    cli = CLI(data_file=data_file)
    cli.run()


if __name__ == "__main__":
    main()

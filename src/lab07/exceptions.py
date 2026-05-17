"""
Пользовательские исключения для предметной области «Недвижимость».
Иерархия: RealEstateError -> ItemNotFoundError, DuplicateItemError,
          ValidationError, StorageError.
"""


class RealEstateError(Exception):
    """Базовое исключение для всех ошибок в системе недвижимости."""
    pass


class ItemNotFoundError(RealEstateError):
    """Объект не найден в коллекции.

    Возникает при поиске или удалении объекта по несуществующему ID.
    """
    def __init__(self, item_id: int = None, message: str = None) -> None:
        if message is None:
            if item_id is not None:
                message = (
                    f"Объект с идентификатором {item_id} не найден в коллекции."
                )
            else:
                message = "Объект не найден в коллекции."
        self.item_id = item_id
        super().__init__(message)


class DuplicateItemError(RealEstateError):
    """Объект с таким идентификатором уже существует.

    Возникает при попытке добавить объект с уже занятым ID.
    """
    def __init__(self, item_id: int = None, message: str = None) -> None:
        if message is None:
            if item_id is not None:
                message = (
                    f"Объект с идентификатором {item_id} уже существует."
                )
            else:
                message = "Объект с таким идентификатором уже существует."
        self.item_id = item_id
        super().__init__(message)


class ValidationError(RealEstateError):
    """Ошибка валидации введённых данных.

    Возникает при некорректных значениях полей.
    """
    def __init__(self, field: str = None, message: str = None) -> None:
        if message is None:
            if field is not None:
                message = f"Некорректное значение поля '{field}'."
            else:
                message = "Ошибка валидации данных."
        self.field = field
        super().__init__(message)


class StorageError(RealEstateError):
    """Ошибка при работе с файловым хранилищем.

    Возникает при невозможности сохранить или загрузить данные.
    """
    def __init__(self, filepath: str = None, message: str = None) -> None:
        if message is None:
            if filepath is not None:
                message = f"Ошибка при работе с файлом '{filepath}'."
            else:
                message = "Ошибка хранилища данных."
        self.filepath = filepath
        super().__init__(message)

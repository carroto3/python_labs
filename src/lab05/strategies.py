"""
Функции-стратегии для сортировки и фильтрации квартир.
Предметная область: Недвижимость.
"""


# ══════════════════════════════════════════════════════════════════════════
# СТРАТЕГИИ СОРТИРОВКИ
# ══════════════════════════════════════════════════════════════════════════

def by_price(apartment):
    """
    Стратегия сортировки по цене аренды.
    
    Args:
        apartment: объект квартиры
        
    Returns:
        float: цена аренды
    """
    return apartment.price


def by_area(apartment):
    """
    Стратегия сортировки по площади.
    
    Args:
        apartment: объект квартиры
        
    Returns:
        float: площадь в м²
    """
    return apartment.area


def by_price_per_sqm(apartment):
    """
    Стратегия сортировки по цене за квадратный метр.
    
    Args:
        apartment: объект квартиры
        
    Returns:
        float: цена за м²
    """
    return apartment.price / apartment.area


def by_rooms(apartment):
    """
    Стратегия сортировки по количеству комнат.
    
    Args:
        apartment: объект квартиры
        
    Returns:
        int: количество комнат
    """
    return apartment.rooms


# ══════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ-ФИЛЬТРЫ
# ══════════════════════════════════════════════════════════════════════════

def is_affordable(apartment, max_price=50000):
    """
    Фильтр: доступные квартиры (цена ниже максимальной).
    
    Args:
        apartment: объект квартиры
        max_price: максимальная цена
        
    Returns:
        bool: True если квартира доступна по цене
    """
    return apartment.price <= max_price


def is_spacious(apartment, min_area=60):
    """
    Фильтр: просторные квартиры (площадь больше минимальной).
    
    Args:
        apartment: объект квартиры
        min_area: минимальная площадь
        
    Returns:
        bool: True если квартира просторная
    """
    return apartment.area >= min_area


def is_residential(apartment):
    """
    Фильтр: только жилые квартиры.
    
    Args:
        apartment: объект квартиры
        
    Returns:
        bool: True если квартира жилая
    """
    # Проверяем наличие атрибута floor (только у ResidentialApartment)
    return hasattr(apartment, 'floor')


def is_commercial(apartment):
    """
    Фильтр: только коммерческие помещения.
    
    Args:
        apartment: объект квартиры
        
    Returns:
        bool: True если помещение коммерческое
    """
    # Проверяем наличие атрибута business_type (только у CommercialApartment)
    return hasattr(apartment, 'business_type')
"""
Базовый класс для квартиры.
"""


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
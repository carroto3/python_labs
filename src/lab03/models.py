"""
Производные классы квартир.
"""

from base import Apartment


class ResidentialApartment(Apartment):
    """Жилая квартира."""

    def __init__(self, address, area, price, rooms, has_balcony, floor):
        super().__init__(address, area, price, rooms)
        self.has_balcony = has_balcony
        self.floor = floor

    def is_suitable_for_family(self, min_rooms):
        """Проверяет подходит ли для семьи."""
        return self.rooms >= min_rooms and self.area >= 40

    def __str__(self):
        balcony = "есть" if self.has_balcony else "нет"
        return f"Жилая квартира: {self.address}, {self.area} м², {self.rooms} комн., этаж {self.floor}, балкон {balcony}, {self.price} руб."


class CommercialApartment(Apartment):
    """Коммерческое помещение."""

    def __init__(self, address, area, price, rooms, business_type, has_parking):
        super().__init__(address, area, price, rooms)
        self.business_type = business_type
        self.has_parking = has_parking

    def calculate_business_cost(self, clients_per_day):
        """Стоимость на одного клиента в день."""
        daily_cost = self.price / 30
        return daily_cost / clients_per_day

    def __str__(self):
        parking = "есть" if self.has_parking else "нет"
        return f"Коммерческое помещение: {self.address}, тип: {self.business_type}, {self.area} м², парковка {parking}, {self.price} руб."
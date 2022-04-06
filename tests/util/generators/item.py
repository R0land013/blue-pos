from model.entity.models import Item
from unittest.mock import create_autospec
from faker import Faker

fake = Faker()


class ItemGenerator:

    @staticmethod
    def generate_items_by_quantity(quantity: int) -> list:
        items = []
        for _ in range(quantity):
            a_item = create_autospec(spec=Item)

            a_item.name = fake.company()
            a_item.description = fake.text()

            items.append(a_item)
        return items

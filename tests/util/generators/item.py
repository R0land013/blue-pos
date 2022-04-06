from model.entity.models import Item
from unittest.mock import create_autospec
from faker import Faker

fake = Faker()


def equals(self, other: Item):
    return self.name == other.name and self.description == other.description


def to_string(self):
    return '[name: "{}", description: "{}"]'.format(self.name, self.description)


class ItemGenerator:

    @staticmethod
    def generate_items_by_quantity(quantity: int) -> list:
        items = []
        for _ in range(quantity):
            a_item = create_autospec(spec=Item)

            a_item.name = fake.company()
            a_item.description = fake.text()
            a_item.__eq__ = equals
            a_item.__str__ = to_string

            items.append(a_item)
        return items

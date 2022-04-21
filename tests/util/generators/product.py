from model.entity.models import Product
from unittest.mock import create_autospec
from faker import Faker

fake = Faker()


def equals(self, other: Product):
    return self.name == other.name and self.description == other.description


def to_string(self):
    return '[name: "{}", description: "{}"]'.format(self.name, self.description)


class ProductGenerator:

    @staticmethod
    def generate_products_by_quantity(quantity: int) -> list:
        products = []
        for _ in range(quantity):
            a_product = Product()

            a_product.name = fake.company()
            a_product.description = fake.text()

            products.append(a_product)
        return products

    @staticmethod
    def generate_one_product() -> Product:
        a_product = Product()
        a_product.name = fake.company()
        a_product.description = fake.text()

        return a_product

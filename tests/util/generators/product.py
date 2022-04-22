from money import Money

from model.entity.models import Product
from faker import Faker

fake = Faker()


class ProductGenerator:

    DEFAULT_MONEY = Money('1.00', 'CUP')

    @staticmethod
    def generate_products_by_quantity(quantity: int) -> list:
        products = []
        for _ in range(quantity):

            a_product = ProductGenerator.generate_one_product()
            products.append(a_product)

        return products

    @staticmethod
    def generate_one_product() -> Product:
        a_product = Product()
        a_product.name = fake.company()
        a_product.description = fake.text()
        a_product.quantity = 0
        a_product.price = ProductGenerator.DEFAULT_MONEY
        a_product.profit = ProductGenerator.DEFAULT_MONEY

        return a_product
